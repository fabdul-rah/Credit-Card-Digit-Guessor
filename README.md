## Credit Card Check Digit (Luhn)

This project computes the **Luhn (mod 10) check digit** for a card number entered **without** its final digit. The algorithm matches real issuer rules for Visa, Mastercard, American Express, and other networks, including **different PAN lengths** (for example, 14 digits before the check digit for 15-digit AmEx, or 15 digits before the check for 16-digit Visa/Mastercard).

### For a portfolio (coursework / minor / admissions)

Use this README to explain **what you built** and **how you work**:

- **Problem** — Many tutorials hard-code “double every other digit from the left,” which is wrong for some real card lengths. This repo implements Luhn from the **right**, so the check digit is correct for typical 16-digit paths **and** 15-digit AmEx-style bodies.
- **Evidence** — Run `pytest` and mention the **step-by-step trace** in the web UI (expand *Show step-by-step Luhn math*) so reviewers can follow the arithmetic. Optionally publish the **`docs/`** build to **GitHub Pages** and link the live site on your résumé (see below).
- **Ethics** — State clearly that you only use **test numbers**, that Luhn is a **checksum** (not proof of a real account), and that you are not collecting or storing card data.

Optional: add your name and a link to a short screen recording in this section when you submit the portfolio.

### Luhn Algorithm Overview

The Luhn algorithm (also known as the mod-10 algorithm) is a checksum formula used to validate a variety of identification numbers, including credit card numbers. It works by performing the following steps:

1. **Starting from the rightmost digit (excluding the check digit)**, double the value of every second digit. If doubling results in a number greater than 9, subtract 9 from the product.
   
2. **Sum all the digits** of the modified numbers obtained in step 1, along with the untouched digits from the original number.
   
3. **Calculate the check digit** that makes the total sum a multiple of 10. This is done by taking the total sum modulo 10, and then subtracting this value from 10.

### Layout

- `luhn.py` — length-correct Luhn check digit and validation.
- `schemes.py` — issuer hints (Visa, Mastercard, AmEx, Discover, Diners, JCB, UnionPay) from the digit prefix.
- `app.py` — Flask web UI and JSON API (local or any Python host).
- `card.py` — command-line interface.
- `docs/` — **static** site for **GitHub Pages** (`index.html`, `css/`, `js/`) — same math as `luhn.py`, runs in the browser (no server).

### GitHub Pages (public website)

GitHub Pages only serves static files. The published app lives in **`docs/`** (HTML, CSS, ES modules). Logic mirrors `luhn.py` / `schemes.py` in JavaScript.

1. Push the repository to GitHub.
2. In the repo: **Settings → Pages → Build and deployment**.
3. **Source**: **Deploy from a branch**.
4. Branch: **`main`** (or your default), folder: **`/docs`**, then **Save**.
5. After a short build, the site is at **`https://<username>.github.io/<repository>/`** (exact URL is shown on the Pages settings screen).

Edit **`docs/index.html`**: replace `YOUR_USERNAME` in the `<meta name="github-repo" content="https://github.com/YOUR_USERNAME/Credit-Card-Digit-Guessor" />` line with your real GitHub username (and repo name if you renamed it).

**Preview `docs/` locally:**

```bash
cd docs && python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/` (use a local server so ES modules load correctly).

### Web interface (Flask, local)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Choose a card network or leave **Auto-detect**; type all digits **except** the check digit to see the computed last digit and full number.

### CLI

```bash
python card.py
```

### Tests

```bash
pytest
```

### API example

```bash
curl -s -X POST http://127.0.0.1:5000/api/check-digit \
  -H "Content-Type: application/json" \
  -d '{"body":"37828224631000","trace":true}'
```

Set `"trace": true` to include a per-digit breakdown (`steps`, `sum_transformed_body`, `check_digit`) for demos or write-ups.

### Requirements

- Python 3.10 or newer (use a virtual environment; see above).

### Notes

- This script is a basic implementation of the Luhn algorithm for educational purposes and should not be used for actual credit card validation or processing.
- Always handle credit card information securely and adhere to relevant security and compliance standards when working with sensitive data.

Please refer to the script for more details on the implementation. For questions or issues, feel free to reach out or submit a pull request.
