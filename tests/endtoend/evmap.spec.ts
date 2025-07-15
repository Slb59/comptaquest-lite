import { test, expect } from '@playwright/test';

test('the logged in user views the filtered map', async ({ page }) => {

    // 2. Access the dashboard
    await page.goto('http://127.0.0.1:8000/');

    // 3. Click on the EscapeVault logo
    await page.locator('a[title="EscapeVault"]').click();

    // 4. Check that you see the map
    await expect(page.locator('.folium-map')).toBeVisible();

    // 5. Select the “house” category
    await page.selectOption('select[name="category"]', 'maison');

    // 6. Check that only “home” POIs are visible
    await expect(page.locator('.folium-marker')).toHaveCount(1);

    // 7. Check available links
    await expect(page.getByRole('link', { name: 'Liste' })).toHaveAttribute('href', '/escapevault/list/');
    await expect(page.getByRole('link', { name: 'Ajout' })).toHaveAttribute('href', '/escapevault/add/');
    await expect(page.getByRole('link', { name: 'Paramètres' })).toHaveAttribute('href', '/escapevault/parameters/');
});
