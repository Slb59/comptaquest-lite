// scripts/login.spec.ts
import { test, expect } from '@playwright/test';

test('Login and save state', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/login/');
    await page.fill('#id_email', 'testuser@test.com');
    await page.fill('#id_password', 'testpass');
    await page.click('button[type="submit"]');

    // wait redirect to dashboard
    await expect(page).toHaveURL('http://127.0.0.1:8000/');

    // save state of authentication
    await page.context().storageState({ path: 'auth/session.json' });
});
