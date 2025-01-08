# Trade and Investment Factsheets Prototype

This repository contains the source code for the <a href="https://trade-and-investment-factsheets.docs.trade.gov.uk/">Trade and Investment Factsheets Prototype</a>.

> [!IMPORTANT]  
> This is prototype for testing purposes only. It exists to experiment with using the [Observable Framework](https://observablehq.com/framework) to publish dashboards of public data.

---

### Contents

- [Running locally](#running-locally)
- [Making and previewing changes in the browser](#making-and-previewing-changes-in-the-browser)
- [Deployment](#deployment)
- [Command reference](#command-reference)
- [Project structure](#project-structure)

---

## Running locally

This is an [Observable Framework](https://observablehq.com/framework) project. To start the local preview server you first need to clone the code:

```bash
git clone git@github.com:uktrade/trade-and-investment-factsheets.git
```

go into the `trade-and-investment-factsheets` folder:

```bash
cd trade-and-investment-factsheets
```

And then run:

```
npm run dev
```

Then visit <http://localhost:3000> to preview the bashboard.

For more information, see <https://observablehq.com/framework/getting-started>.


## Making and previewing changes in the browser

It's possible to make changes to this dashboard directly in the [github.dev web-based editor](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor), and to preview changes before changing the [production dashboard](https://trade-and-investment-factsheets.docs.trade.gov.uk/). 

While the feedback cycle of this process is slow, this process is suitable if you are not able to run this dashboard locally.

> [!CAUTION]  
> Previews are just like everything else in this repository: open to the world.

The steps to make changes are in the [Using source control section of the github.dev documentation](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor#using-source-control), but briefly:

1. When viewing the repository in your browser, for example the page you're currently reading, press "." (full stop) to start the web-based editor.

2. Create a new branch, for example "feat/change-title". 

3. Make changes as needed.

4. Commit and push. The commit message can be brief, but should be accurate.

5. Make a pull request from your branch. It should appear at https://github.com/uktrade/trade-and-investment-factsheets/pulls.

To then preview changes:

6. Wait for a comment to appear in the pull request for your change that contains a link to the preview. Click the link to see the preview.

   Note that the comment appears a few moments _before_ the preview is ready. If you click the link very soon after it appears, you may arrive at a 404 error page. If this happens wait a few moments and refresh.

   If there is an error when building the preview, the comment will not appear. Errors should be visible in the [log of workflows for the "GitHub pages: deploy preview" action](https://github.com/uktrade/trade-and-investment-factsheets/actions/workflows/github-pages-deploy-preview.yml).

If you need to make changes, you should be able to repeat steps 3 and 4 above for your branch, and then wait again for the preview to be updated so you can see the effects of your changes.

Then before merging the PR:

7. Make sure the pull request title and description are accurate, and describe what this change does from a end user point of view, why it's being done, and how.


## Deployment

The dashboard is hosted on GitHub pages, and deployed automatically on every push or merge to the main branch, and on a daily schedule. See the ["GitHub pages: deploy main" workflow](.github/workflows/github-pages-deploy-main.yml) for details.


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
