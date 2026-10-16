module.exports = {
    extends: '@wagtail/eslint-config-wagtail',
    env: {
        browser: true,
    },
    overrides: [
        {
            files: ['**/*.test.js'],
            env: { jest: true },
        },
    ],
};
