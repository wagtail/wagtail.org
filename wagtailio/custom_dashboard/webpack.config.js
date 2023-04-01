const path = require('path');

module.exports = {
    entry: './index.tsx',
    devServer: {
        static: '../static_compiled/js',
        hot: true,
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.svg$/,
                use: ['@svgr/webpack'],
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: 'dashboard.js',
        path: path.resolve(__dirname, '../static_compiled/js'),
        clean: true
    },
}
