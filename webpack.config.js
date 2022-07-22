const path = require('path');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const sass = require('sass');
const ESLintPlugin = require('eslint-webpack-plugin');
const StylelintPlugin = require('stylelint-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

const projectRoot = 'wagtailio';

const options = {
  entry: {
    main: `./${projectRoot}/static/js/main.js`,
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
  },
  output: {
    path: path.resolve(`./${projectRoot}/static_compiled/`),
    filename: 'js/[name].js',
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: 'img',
          context: path.resolve(`./${projectRoot}/static/`),
          to: path.resolve(`./${projectRoot}/static_compiled/img`),
        },
      ],
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',
    }),
    new ESLintPlugin({
      failOnError: false,
      lintDirtyModulesOnly: true,
      emitWarning: true,
    }),
    new StylelintPlugin({
      failOnError: false,
      lintDirtyModulesOnly: true,
      emitWarning: true,
      extensions: ['scss'],
    }),
    //  Automatically remove all unused webpack assets on rebuild
    new CleanWebpackPlugin(),
    new WebpackManifestPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.(js|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'ts-loader',
        },
      },
      {
        test: /\.(scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                sourceMap: true,
                plugins: () => [
                  autoprefixer(),
                  cssnano({
                    preset: 'default',
                  }),
                ],
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              implementation: sass,
              sassOptions: {
                outputStyle: 'compressed',
              },
            },
          },
        ],
      },
    ],
  },
};

const webpackConfig = (environment, argv) => {
  const isProduction = argv.mode === 'production';

  options.mode = isProduction ? 'production' : 'development';

  if (!isProduction) {
    // https://webpack.js.org/configuration/stats/
    const stats = {
      // Tells stats whether to add the build date and the build time information.
      builtAt: false,
      // Add chunk information (setting this to `false` allows for a less verbose output)
      chunks: false,
      // Add the hash of the compilation
      hash: false,
      // `webpack --colors` equivalent
      colors: true,
      // Add information about the reasons why modules are included
      reasons: false,
      // Add webpack version information
      version: false,
      // Add built modules information
      modules: false,
      // Show performance hint when file size exceeds `performance.maxAssetSize`
      performance: false,
      // Add children information
      children: false,
      // Add asset Information.
      assets: false,
    };

    options.stats = stats;

    // Create JS source maps in the dev mode
    // See https://webpack.js.org/configuration/devtool/ for more options
    options.devtool = 'inline-source-map';

    // See https://webpack.js.org/configuration/dev-server/.
    options.devServer = {
      // Enable gzip compression for everything served.
      compress: true,
      host: '0.0.0.0',
      port: 3000,
      proxy: {
        context: () => true,
        target: 'http://localhost:8000',
      },
      client: {
        logging: 'error',
        // Shows a full-screen overlay in the browser when there are compiler errors.
        overlay: true,
      },
      static: {
        directory: path.resolve(__dirname, 'static'),
      },
      devMiddleware: {
        // Write compiled files to disk. This makes live-reload work on both port 3000 and 8000.
        writeToDisk: true,
        stats,
        index: '',
        publicPath: '/static/',
      },
    };
  }

  return options;
};

module.exports = webpackConfig;
