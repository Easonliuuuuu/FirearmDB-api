# FirearmDB API

This repository contains the source code for the FirearmDB API, a serverless REST API that provides detailed information about firearms, cartridges, manufacturers, and their involvement in historical conflicts.

The application is built with Python using the FastAPI framework and is deployed on AWS Lambda using the AWS Serverless Application Model (SAM). It features a fully automated CI/CD pipeline using GitHub Actions for testing and deployment.


### Authentication
- Register: `POST /api/v1/register` with JSON `{ "email": "user@example.com", "password": "..." }`
- Login: `POST /api/v1/token` with form fields `username`, `password`
- Use the returned token for authenticated requests:
  - Header: `Authorization: Bearer <access_token>`

### Rate Limits
- Authenticated: 5 requests per minute
- Anonymous: 2 requests per minute

### Common Headers
- `Content-Type: application/json`
- `Authorization: Bearer <access_token>` where required

## Endpoints
Base prefix: `/api/v1`

### Authentication
- `POST /register`
  - Body: `{ "email": string, "password": string }`
  - 200 → `{ id, email }`
- `POST /token`
  - Form: `username`, `password`
  - 200 → `{ access_token, token_type: "bearer" }`

### Firearm
- `GET /firearm/` → list firearms
- `GET /firearm/search?name=<query>` → search by name (partial, case-insensitive)
- `GET /firearm/{firearm_id}` → firearm by id
- `GET /firearm/{firearm_id}/wars` → wars for firearm
- `GET /firearm/{firearm_id}/cartridges` → cartridges for firearm
- `GET /firearm/{firearm_id}/manufacturers` → manufacturers for firearm

### Cartridge
- `GET /cartridge/` → list cartridges
- `GET /cartridge/search?name=<query>` → search
- `GET /cartridge/{cartridge_id}` → cartridge by id
- `GET /cartridge/{cartridge_id}/firearms` → firearms for cartridge
- `GET /cartridge/{cartridge_id}/firearms/names` → firearm ids/names for cartridge

### Type
- `GET /type/` → list types
- `GET /type/search?name=<query>` → search
- `GET /type/{type_id}` → type by id
- `GET /type/{type_id}/firearms` → firearms for type
- `GET /type/{type_id}/firearms/names` → firearm ids/names for type

### Manufacturer
- `GET /manufacturer/` → list manufacturers
- `GET /manufacturer/search?name=<query>` → search
- `GET /manufacturer/{manufacturer_id}` → manufacturer by id
- `GET /manufacturer/{manufacturer_id}/firearms` → firearms for manufacturer
- `GET /manufacturer/{manufacturer_id}/firearms/names` → firearm ids/names for manufacturer

### War
- `GET /war/` → list wars
- `GET /war/search?query=<text>` → search by name
- `GET /war/{war_id}` → war by id
- `GET /war/{war_id}/firearms` → firearms used in war
- `GET /war/{war_id}/firearms/names` → firearm ids/names used in war

## Errors
- 400: Bad request (e.g., missing query parameters)
- 401: Authentication failed or missing token
- 404: Resource not found
- 429: Too many requests (rate limit exceeded)

## Notes
- CORS is enabled.
- Some endpoints are rate limited; authenticate to receive higher limits.
