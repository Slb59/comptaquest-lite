import { test, expect } from '@playwright/test';
test.use({ storageState: 'tests/auth/session.json' });
test('the logged in user views the filtered map', async ({ page }) => {

    // 2. Access the dashboard
    await page.goto('http://127.0.0.1:8001/');

    // 3. Click on the EscapeVault logo
    await page.locator('a[title="EscapeVault"]').click();

    // 4. Check that you see the map
    const iframeElement = await page.waitForSelector('iframe');
    const frame = await iframeElement.contentFrame();
    if (!frame) {
        throw new Error('Impossible d’accéder au contenu de l’iframe.');
    }
    await frame.waitForSelector('.folium-map', { state: 'visible', timeout: 20000 });
    if (frame) {
        const html = await frame.content();
        console.log(html); // Pour voir si la carte est bien chargée
    }
    // await expect(page.locator('.leaflet-marker-icon')).toHaveCount(4);


    // 5. Select the “house” category
    await page.selectOption('select[id="id_category"]', 'Maison');

    // 6. Check that only “home” POIs are visible
    // await expect(page.locator('.leaflet-marker-icon')).toHaveCount(1);

    // 7. Check available links
    await expect(page.getByRole('link', { name: 'Liste des positions' })).toHaveAttribute('href', '/escapevault/list/');
    await expect(page.getByRole('link', { name: 'Nouvelle position' })).toHaveAttribute('href', '/escapevault/add/');
    await expect(page.getByRole('link', { name: 'Paramètres' })).toHaveAttribute('href', '/escapevault/parameters/');
});
