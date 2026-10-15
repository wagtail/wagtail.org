// See https://jestjs.io/docs/configuration
module.exports = {
    testEnvironment: 'jsdom',
    testPathIgnorePatterns: ['/node_modules/', '/static_compiled/'],
    collectCoverageFrom: ['wagtailio/static/js/**/*.{js,ts,tsx}'],
    transform: {
        '^.+\\.(js|ts|tsx)$': 'ts-jest',
    },
};
