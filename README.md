# Angular Weather Frontend

Modern Angular weather UI for a Python Flask/FastAPI backend.

## API Contract

The frontend calls:

```text
GET http://127.0.0.1:5050/weather?city=London&unit=celsius
```

Expected response:

```json
{
  "city": "London",
  "temperature": 23,
  "windspeed": 12,
  "condition": "Partly cloudy",
  "weathercode": 2
}
```

Change the backend URL in `src/environments/environment.ts` if your API runs elsewhere.

## Project Structure

```text
src/
  app/
    core/
      models/weather.model.ts
      services/weather.service.ts
      services/recent-searches.service.ts
    features/
      search/
      weather/
    shared/
      loading-spinner/
    app.config.ts
    app.html
    app.scss
    app.ts
  environments/
    environment.ts
    environment.development.ts
```

## Commands

Create a fresh Angular app:

```bash
ng new weather-frontend --standalone --style=scss --routing=false
```

Install dependencies:

```bash
npm install
```

Run the app:

```bash
npm start
```

Open `http://localhost:4200`.

## Deploying The Frontend To Vercel

Deploy the Angular frontend as a separate Vercel project from the backend API.

Recommended Vercel settings:

```text
Root Directory: weather-frontend
Framework Preset: Angular
Build Command: npm run build
Output Directory: dist/weather-frontend/browser
Install Command: npm install
```

Before deploying, update `src/environments/environment.ts` and
`src/environments/environment.development.ts` so `apiUrl` points to your deployed API URL:

```ts
export const environment = {
  production: false,
  apiUrl: 'https://YOUR_API_DEPLOYMENT.vercel.app',
};
```

Build for production:

```bash
npm run build
```

Run tests:

```bash
npm test
```

## Features

- Standalone Angular components with SCSS.
- Reactive city search with recent searches stored in `localStorage`.
- `HttpClient` API integration for `/weather`.
- Celsius/Fahrenheit unit toggle.
- Weather code mapping for clear, cloudy, rain, thunderstorm, snow, and fog.
- Glassmorphism card, animated gradients, loading spinner, error state, and responsive mobile-first layout.
- Light/dark visual mode toggle.
