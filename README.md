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
    - [Local Environment](#local-environment-setup)
    - [Environment Variables](#environment-variables)
    - [Alembic and Faker data](#alembic-migrations-and-faker-data-population)
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

## Development Environment Setup

### Prerequisites
All required packages are listed in [requirements.txt](requirements.txt) and can be installed locally using the following command:
![image](https://github.com/crobin27/music-api/assets/76970281/1f62f0b4-d099-4687-9606-6ade12ebcb81)

### Local Environment Setup
For local setup and testing, we leveraged Supabase's local database setup and Docker to run the container locally. This local setup proved crucial in testing key features without corrupting the staging or production databases. Follow the steps listed [here](https://supabase.com/docs/guides/getting-started/local-development) in the Supabase documentation to get started.

### Environment Variables
Upon creation of the local Docker container and Postgres database, the following environment variables must be configured in a .env file located in the root of the project. The following fields must be included to ensure a stable connection to the local database. 
```
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_SERVER="localhost"
POSTGRES_PORT="54322"
POSTGRES_DB="postgres"
```

In addition to the Postgres connection variables, a Weather API Key must be obtained and set. Information on obtaining an API key can be found here(https://www.weatherapi.com/signup.aspx). Once the key is obtained, set the environment variable like below:
```
WEATHER_API_KEY="<your_api_key>"
```

### Alembic Migrations and Faker data population
In order to handle database migrations as our schema evolved, we made use of the alembic library's built in autogeneration functionality. More information can be found here(https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

To update the local database to the most recent migration, run
![image](https://github.com/crobin27/music-api/assets/76970281/547337db-2ad0-4732-8f0d-1dcece8778a7)

We additionally created an autopopulation script that creates just over a million fake rows of data using the python 'faker' library. This step was crucial in testing the database with large sums of data. To populate with fake data, run
![image](https://github.com/crobin27/music-api/assets/76970281/30b181b8-95b9-4975-bbdd-9d983fe37d7c)


### Run the API
Run following on your terminal:
```
vercel dev
```
