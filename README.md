# UK trade quotas dashboard

This repository contains the source code for the <a href="https://uktrade.github.io/uk-trade-quotas-dashboard/">UK trade quotas dashboard</a>.

The dashboard sources data from the <a class="govuk-link govuk-link--no-visited-state" href="https://www.data.gov.uk/dataset/4a478c7e-16c7-4c28-ab9b-967bb79342e9/uk-trade-quotas">"UK trade quotas" dataset published on data.gov.uk</a>, which in turn sources data from the <a href="https://data.api.trade.gov.uk/">Department for Business and Trade Data API</a>.

> [!IMPORTANT]  
> This is prototype for testing purposes only. It exists to experiment with using the [Observable Framework](https://observablehq.com/framework) to publish dashboards of public data.

---

### Contents

- [Running locally](#running-locally)
- [Deployment](#deployment)
- [Command reference](#command-reference)
- [Project structure](#project-structure)

---

## Running locally

This is an [Observable Framework](https://observablehq.com/framework) project. To start the local preview server you first need to clone the code:

```bash
git clone git@github.com:uktrade/uk-trade-quotas-dashboard.git
```

go into the `uk-trade-quotas-dashboard` folder:

```bash
cd uk-trade-quotas-dashboard
```

And then run:

```
npm run dev
```

Then visit <http://localhost:3000> to preview the bashboard.

For more information, see <https://observablehq.com/framework/getting-started>.


## Deployment

The dashboard is hosted on GitHub pages, and deployed automatically on every push or merge to the main branch, and on a daily schedule. See the <a href="./.github/workflows/deploy-to-github-pages.yml">Deploy to GitHub Pages workflow</a> for details.


## Command reference

| Command           | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `npm install`            | Install or reinstall dependencies                        |
| `npm run dev`        | Start local preview server                               |
| `npm run build`      | Build your static site, generating `./dist`              |
| `npm run deploy`     | Deploy your project to Observable                        |
| `npm run clean`      | Clear the local data loader cache                        |
| `npm run observable` | Run commands like `observable help`                      |


## Project structure

The project structure follows the usual Observable Framework structure. An example of such a structure is:

```ini
.
├─ src
│  ├─ components
│  │  └─ timeline.js           # an importable module
│  ├─ data
│  │  ├─ launches.csv.js       # an example data loader
│  │  └─ events.json           # an example static data file
│  ├─ example-dashboard.md     # a page
│  ├─ example-report.md        # another page
│  └─ index.md                 # the home page
├─ .gitignore
├─ observablehq.config.js      # the project config file
├─ package.json
└─ README.md
```

**`src`** - This is the “source root” — where the source files live. Pages go here. Each page is a Markdown file. Observable Framework uses [file-based routing](https://observablehq.com/framework/routing), which means that the name of the file controls where the page is served. You can create as many pages as you like. Use folders to organize your pages.

**`src/index.md`** - This is the home page for the site. You can have as many additional pages, but there must be a home page.

**`src/data`** - You can put [data loaders](https://observablehq.com/framework/loaders) or static data files anywhere in your source root, but it's recommended to put them here.

**`src/components`** - You can put shared [JavaScript modules](https://observablehq.com/framework/javascript/imports) anywhere in the source root, but it's recommended to put them here. This helps you pull code out of Markdown files and into JavaScript modules, making it easier to reuse code across pages, write tests and run linters, and even share code with vanilla web applications.

**`observablehq.config.js`** - This is the [project configuration](https://observablehq.com/framework/config) file, such as the pages and sections in the sidebar navigation, and the project’s title.
