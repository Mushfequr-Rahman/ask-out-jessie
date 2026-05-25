# Jessie Date Invitation

A static GitHub Pages site for asking Jessie out, with cute generated imagery, a moving "No" button, and a separate booking page.

## Free Notification Setup

Use Formspree's free tier:

1. Go to <https://formspree.io>.
2. Create a free form and verify your email.
3. Copy the form endpoint. It looks like `https://formspree.io/f/xabcwxyz`.
4. Open `script.js` and paste it into `CONFIG.formEndpoint`.

Optional fallback: put your email in `CONFIG.fallbackEmail`. If no Formspree endpoint is set, the form opens an email draft instead. Formspree is better for GitHub Pages because it sends the details without needing a backend.

## GitHub Pages

1. Push this folder to a GitHub repository.
2. In GitHub, open Settings > Pages.
3. Set the source to the main branch and root folder.
4. Visit the Pages URL after it finishes deploying.

## Files

- `index.html`: page structure and form fields.
- `booking.html`: date and time form.
- `styles.css`: responsive visual design.
- `script.js`: yes/no behavior and form submission.
- `assets/cute-hero.png`: generated landing image.
- `assets/cute-booking.png`: generated booking image.
