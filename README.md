# Music API

## Authors
Cole Robinson (colerobinson1112@gmail.com)

Geoff Blaylock (gblaylock2024@gmail.com)

<details open="open">
<summary>Table of Contents</summary>
<br>

- [About](#about)
- [Vercel Links](#vercel-links)
- [Documentation Files](#documentation-files)
- [Development Environment Setup](#development-environment-setup)
    - [Prerequisites](#prerequisites)
    - [Local Environment](#set-up-your-local-environment)
    - [Environment Variables](#environment-variables)
    - [Alembic and Faker data](#alembic-and-faker-data)
    - [Run the API](#run-the-api)
</details>

## About
Welcome to our Music API. Our Music Discovery API provides a seamless integration of real-time weather data with user-inputted vibe for personalized music recommendations. When a user inputs their current location, our API retrieves the current weather data for that specific area. Combined with the user's indicated 'vibe' — a mood or feeling they wish their music to align with — our system uses a sophisticated algorithm to curate songs and albums that best fit the given combination. Users have the option to create playlists, add music information, and obtain music reccomendations. 

## Vercel Links
Our API Endpoints are deployed using Vercel to provide continuous integration and deployment throughout the development process while always maintaining a stable production build. Below are links to our production and staging API endpoints:
- Production: https://music-api-git-prod-crobin27.vercel.app
- Staging: https://music-api-git-staging-crobin27.vercel.app

## Documentation Files
Listed below are documents we have gathered that provide further insight into the development of this API.

For a comprehensive overview of each of the endpoints designed, check out our [Technical Specification](Documentation/Technical_Specification.pdf).

To keep track of our table relationships, we created an Entity-Relationship Diagram to provide a visual representation of our database tables. Using crow's foot notation, we ensured that each entity relationship is accounted for. Check out our [ER Diagram](Documentation/Dog_Trainer_ER_Diagram.pdf).

We've identified the issues that can arise from the complex interactions of transactions in our database when there's no concurrency control. In response, we've designed a solution to ensure the isolation of our transactions. Check out [Isolation Levels](Documentation/Isolation_Levels.pdf) to learn more.

To view the indexes we created to make our SQL execution time faster, check out [Indexes](Documentation/i.pdf).

## Local Setup

### Prerequisites
All required packages are listed in [requirements.txt](requirements.txt) and can be installed locally using the following command:
![image](https://github.com/crobin27/music-api/assets/76970281/1f62f0b4-d099-4687-9606-6ade12ebcb81)

### Set up your local environment
Follow steps listed [here](https://supabase.com/docs/guides/getting-started/local-development) in the Supabase documentation.

### Environment Variables
Create a .env file with these variables:
```
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_SERVER="localhost"
POSTGRES_PORT="54322"
POSTGRES_DB="postgres"
```

### Alembic and Faker data
To rebuild alembic and populate with fake data, run:
```
sh populate_alembic.sh
```

### Run the API
Run following on your terminal:
```
vercel dev
```
