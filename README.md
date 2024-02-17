
# Archive Management System 

The service enables the management of archived documents and includes the following functionalities:
- Registration of documents received in the archive
- Storage and retrieval of documents
- Create and execute document scanning and retrieval requests
- Time and status control

Project based on Django, DRF, Vue3, Docker

Web-site: [ams-service](amsservice.online)

## Requirements
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Node](https://nodejs.org/en/download/package-manager)
- [Vite](https://installati.one/install-vite-ubuntu-20-04/)

## Project Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PvtJoker91/ams.git
   cd ams

2. Install all required packages in `Requirements` section

3. Build Vue frontend
   ```bash
   cd ams_front
   npm run build
   cd ..

4. Configure your environment settings:
   - rename .env.template to .env
   - set your variables in .env

### Implemented Commands

* `make app` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make app-down` - down application and all infrastructure
* `make storages` - up only storages. you should run your application locally for debugging/developing purposes
* `make storages-logs` - follow the logs in storages containers
* `make storages-down` - down all infrastructure

### Most Used Django Specific Commands

* `make migrations` - make migrations to models
* `make migrate` - apply all made migrations
* `make collectstatic` - collect static
* `make superuser` - create admin user
