# Stack Reference — Meteo Tartufai

## Stack scelto

| Componente | Tecnologia | Versione/Docs |
|---|---|---|
| **Backend** | FastAPI (Python) | `/websites/fastapi_tiangolo` |
| **Frontend** | React + Vite + Tailwind CSS | Vite: `/vitejs/vite`, Tailwind: `/websites/tailwindcss` |
| **Mappa** | MapLibre GL JS | `/maplibre/maplibre-gl-js` |
| **Database** | PostgreSQL + PostGIS | PostGIS: `postgis/postgis:16-3.4` |
| **ORM** | SQLAlchemy 2.0 asincrono | `/websites/sqlalchemy_en_20` |
| **Geo ORM** | GeoAlchemy2 | `/geoalchemy/geoalchemy2` |
| **Auth** | JWT con python-jose | `/mpdavis/python-jose` |
| **Password** | pwdlib (argon2) | — |
| **Meteo** | Open-Meteo API | `/websites/open-meteo_en` |
| **Grafici** | Recharts | `/recharts/recharts` |
| **Deploy** | Docker Compose | `/docker/compose` |
| **Migrations** | Alembic | — |

---

## 1. FastAPI

### Struttura del progetto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, include routers
│   ├── config.py            # Settings (DB, JWT secret, etc.)
│   ├── dependencies.py      # Dipendenze (get_current_user, get_db)
│   ├── database.py          # Engine, session factory
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── spot.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── spot.py
│   ├── routers/             # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── spots.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── meteo.py         # Open-Meteo integration
├── alembic/                 # Migrations
├── requirements.txt
├── Dockerfile
└── alembic.ini
```

### Avvio app

```python
# main.py
from fastapi import FastAPI
from app.routers import auth, spots

app = FastAPI(title="Meteo Tartufai")
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(spots.router, prefix="/api/spots", tags=["spots"])
```

### JWT Auth (con python-jose + pwdlib)

```python
# dependencies.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
pwd_hash = PasswordHash.recommended()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # get user from DB...
    return user
```

### Background tasks

```python
from fastapi import BackgroundTasks

@app.post("/api/spots/{id}/refresh")
async def refresh_weather(id: int, bg: BackgroundTasks):
    bg.add_task(fetch_and_store_weather, spot_id=id)
    return {"message": "refresh started"}
```

Per cron jobs programmati: usare `APScheduler` o un container separato che chiama endpoint interni.

### Dipendenze (requirements.txt)

```
fastapi>=0.115.0
uvicorn[standard]
sqlalchemy[asyncio]>=2.0
asyncpg
geoalchemy2
alembic
python-jose[cryptography]
pwdlib[argon2]
httpx
pydantic-settings
```

---

## 2. Vite + React + Tailwind

### Setup iniziale

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @tailwindcss/vite tailwindcss maplibre-gl recharts
```

### vite.config.ts

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': 'http://backend:8000'
    }
  }
})
```

### CSS principale (src/index.css)

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

### Uso Tailwind in React

```tsx
<div className="flex flex-col p-4 md:p-6 lg:p-8 dark:bg-gray-900">
  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
    Dashboard
  </h1>
</div>
```

---

## 3. MapLibre GL JS

### Installazione

```bash
npm install maplibre-gl
```

### Inizializzazione mappa

```tsx
import { useRef, useEffect } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

function Map() {
  const mapContainer = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const map = new maplibregl.Map({
      container: mapContainer.current!,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [11.5, 44.5],  // centro Italia
      zoom: 7
    })
    return () => map.remove()
  }, [])

  return <div ref={mapContainer} className="w-full h-full" />
}
```

### Aggiungere marker

```ts
map.on('load', () => {
  new maplibregl.Marker({ color: '#10b981' })
    .setLngLat([11.5, 44.5])
    .setPopup(new maplibregl.Popup().setText('Spot A'))
    .addTo(map)
})
```

### Heatmap layer

```ts
map.on('load', () => {
  map.addSource('precipitazioni', {
    type: 'geojson',
    data: '/api/spots/heatmap-data'
  })

  map.addLayer({
    id: 'precipitazioni-heat',
    type: 'heatmap',
    source: 'precipitazioni',
    paint: {
      'heatmap-weight': ['get', 'mm_pioggia'],
      'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
      'heatmap-color': [
        'interpolate', ['linear'], ['heatmap-density'],
        0, 'rgba(33,102,172,0)',
        0.2, 'rgb(103,169,207)',
        0.4, 'rgb(209,229,240)',
        0.6, 'rgb(253,219,199)',
        0.8, 'rgb(239,138,98)',
        1, 'rgb(178,24,43)'
      ],
      'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 5, 9, 30],
      'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 7, 1, 9, 0.5]
    }
  })
})
```

Per stili mappa con terreno migliori:
- `https://demotiles.maplibre.org/style.json` (base, gratuito)
- Stili OpenFreeMap (migliori per boschi/montagne)

---

## 4. SQLAlchemy 2.0 asincrono

### Configurazione database

```python
# database.py
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:pass@db:5432/meteo"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Modelli 2.0 style

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from geoalchemy2 import Geometry, WKBElement

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    spots: Mapped[list["Spot"]] = relationship(back_populates="user")

class Spot(Base):
    __tablename__ = "spots"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=False
    )
    radius: Mapped[int] = mapped_column(default=500)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="spots")
```

### Query spaziali

```python
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

# Creare punto
point = from_shape(Point(11.5, 44.5), srid=4326)

# ST_DWithin: trova spot entro 500m
spots = await session.execute(
    select(Spot).where(
        func.ST_DWithin(Spot.location, point, 500)
    )
)

# ST_Contains: verifica se punto è dentro un poligono
query = select(Spot).where(func.ST_Contains(Spot.geom, point))
```

### Migrations con Alembic

```bash
alembic init alembic
# configurare sqlalchemy.url = postgresql://user:pass@db:5432/meteo (sync!)
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

## 5. GeoAlchemy2 — Riferimento tipi

| Tipo PostgreSQL | GeoAlchemy2 |
|---|---|
| `GEOMETRY(Point, 4326)` | `Geometry("POINT", srid=4326)` |
| `GEOGRAPHY(Point, 4326)` | `Geography("POINT", srid=4326)` |
| `GEOMETRY(Polygon, 4326)` | `Geometry("POLYGON", srid=4326)` |

Usare `GEOGRAPHY` per query in metri (ST_DWithin funziona in metri su geography, in gradi su geometry).

---

## 6. Open-Meteo API

### Endpoint

**Previsioni (7 giorni):**
```
GET https://api.open-meteo.com/v1/forecast
  ?latitude=44.5
  &longitude=11.5
  &daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max
  &daily=precipitation_sum
  &timezone=Europe/Rome
  &forecast_days=7
```

**Storico (archivio ERA5 dal 1940):**
```
GET https://archive-api.open-meteo.com/v1/archive
  ?latitude=44.5
  &longitude=11.5
  &daily=precipitation_sum
  &start_date=2026-06-28
  &end_date=2026-07-28
  &timezone=Europe/Rome
```

### Parametri utili per precipitazioni

| Parametro | Descrizione |
|---|---|
| `daily=precipitation_sum` | Cumulato pioggia giornaliero (mm) |
| `daily=precipitation_hours` | Ore di pioggia |
| `daily=precipitation_probability_max` | Probabilità pioggia max (%) |
| `hourly=precipitation` | Pioggia oraria (mm) |
| `hourly=soil_moisture_0_to_1cm` | Umidità terreno superficie |

### Chiamata da Python

```python
import httpx

async def fetch_weather(lat: float, lon: float):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Rome",
        "forecast_days": 7
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        resp.raise_for_status()
        return resp.json()
```

Niente API key per uso non commerciale.

---

## 7. Docker Compose

### docker-compose.yml

```yaml
services:
  db:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: meteo
      POSTGRES_USER: meteo
      POSTGRES_PASSWORD: ${DB_PASSWORD:-meteo_dev}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U meteo"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://meteo:meteo_dev@db:5432/meteo
      SECRET_KEY: ${SECRET_KEY:-dev-secret-key-change-in-production}
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - path: ./backend
          action: rebuild

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: /api
    depends_on:
      - backend
    develop:
      watch:
        - path: ./frontend/src
          action: sync
        - path: ./frontend/package.json
          action: rebuild

volumes:
  pgdata:
```

### Sviluppo con hot reload

```bash
docker compose watch
```

---

## 8. Recharts — Grafici React

### LineChart per precipitazioni

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface RainData {
  date: string
  mm: number
}

function RainChart({ data }: { data: RainData[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis unit=" mm" />
        <Tooltip />
        <Line type="monotone" dataKey="mm" stroke="#3b82f6" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

### BarChart per cumulati settimanali

```tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

function WeeklyRainBar({ data }: { data: RainData[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data}>
        <XAxis dataKey="date" />
        <YAxis unit=" mm" />
        <Tooltip />
        <Bar dataKey="mm" fill="#3b82f6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
```

### AreaChart per accumulo progressivo

```tsx
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

function CumulativeRain({ data }: { data: RainData[] }) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <AreaChart data={data}>
        <XAxis dataKey="date" />
        <YAxis unit=" mm" />
        <Tooltip />
        <Area type="monotone" dataKey="mm" stroke="#2563eb" fill="#93c5fd" fillOpacity={0.3} />
      </AreaChart>
    </ResponsiveContainer>
  )
}
```

---

## 9. Convenzioni di progetto

### Backend
- API REST con prefisso `/api/`
- Schemi Pydantic per request/response (non esporre modelli DB)
- Dipendenze FastAPI per auth e DB session
- Servizi separati per business logic (meteo, correlazione)
- Test con pytest + pytest-asyncio + httpx

### Frontend
- TypeScript rigoroso
- Componenti funzione con hooks
- Stili con Tailwind utility classes (niente CSS custom se evitabile)
- Componenti UI atomici seguiti da feature components
- Stato globale con React Context o Zustand (semplice)

### Database
- Migrations con Alembic
- `created_at` / `updated_at` su ogni tabella
- PostGIS per dati geospaziali
- RLS (Row-Level Security) per isolamento multi-tenancy in futuro
