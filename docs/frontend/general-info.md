# Frontend tooling

## What's included

-   [Sass](http://sass-lang.com/) CSS with [auto-prefixing](https://github.com/postcss/autoprefixer).
-   [TypeScript](https://www.typescriptlang.org/) for ES2015+ JavaScript, and TypeScript support.
-   [webpack-dev-server](https://v4.webpack.js.org/configuration/dev-server/) for autoreloading.
-   [Webpack](https://webpack.js.org/) for module bundling.
    -   With `ts-loader` to process JavaScript and TypeScript.
    -   With `css-loader`, `postcss-loader`, and `sass-loader` to process stylesheets.
-   CSS linting with `stylelint`
-   JS linting with `eslint`

## Developing with it

-   To start the development environment, follow instruction in README.md in the project root
-   Source files for developing your project are in `static` and the distribution folder for the compiled assets is `static_compiled`. Don't make direct changes to the `static_compiled` directory as they will be overwritten.

# Django Pattern Library

The site uses [Django Pattern Library](https://torchbox.github.io/django-pattern-library/) which can be found at http://localhost:8000/pattern-library. We encourage keeping this populated and up to date. Along with a Components and Pages directory there is also a Style Guide directory which contains templates that are intended to be used to showcase available patterns and styles.

# Iconography

The site uses icons throughout the build, a comprehensive list can be found [in the Pattern Library](http://localhost:8000/pattern-library/pattern/patterns/styleguide/icons.html). SVG optimsation is encouraged before being added to build - one library for doing this is [SVGO](https://github.com/svg/svgo).

# Grid

The site uses a grid system across 3 breakpoints:

-   Large: 2 gutter columns, 5 main columns
-   Medium: 2 gutter columns, 3 main columns
-   Small: 2 gutter columns, 2 main columns

To use the system wrap a component in `<div class="grid">` and then align your component accordingly.
