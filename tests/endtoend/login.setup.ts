// scripts/login.spec.ts
import { test, expect } from '@playwright/test';

test('Login and save state', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/login/');
    await page.fill('#id_username', 'test.user@test.com');
    await page.fill('#id_password', 'motdepasse');
    await page.click('input[type="submit"]');

    // wait redirect to dashboard
    await expect(page).toHaveURL('http://127.0.0.1:8000/');

    // save state of authentication
    await page.context().storageState({ path: 'tests/auth/session.json' });
});
