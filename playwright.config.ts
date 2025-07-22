// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
    // prevent to execute tests in parallel
    fullyParallel: false,
    workers: 1,

    projects: [
        {
            name: 'setup',
            testMatch: 'tests/endtoend/login.setup.ts',
        },
        {
            name: 'e2e',
            testMatch: 'tests/endtoend/**/*.spec.ts',
            use: {
                storageState: 'tests/auth/session.json',
            },
        },
    ],
});
