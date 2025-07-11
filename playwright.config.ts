// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
    use: {
        baseURL: 'http://127.0.0.1:8000',
        storageState: 'auth/session.json',
        headless: true,
    },
    testDir: './tests',
});
