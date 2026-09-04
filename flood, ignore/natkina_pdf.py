import pypdf
from weasyprint import HTML

html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
    background-color: #faf9f6;
  }
  
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #2c2c2c;
    background-color: #faf9f6;
    font-size: 8.2pt;
    line-height: 1.35;
  }

  /* Header Section */
  .header-container {
    text-align: center;
    border-bottom: 1px solid #d8d2c7;
    padding-bottom: 8px;
    margin-bottom: 10px;
    position: relative;
  }

  .swiss-badge {
    display: inline-block;
    background: #8c734b;
    color: #ffffff;
    font-size: 6.5pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 2px 8px;
    border-radius: 2px;
    margin-bottom: 4px;
  }

  .brand-logo {
    font-family: 'Georgia', serif;
    font-size: 26pt;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #1a1a1a;
    font-weight: normal;
    line-height: 1;
    margin-bottom: 3px;
  }

  .brand-location {
    font-size: 7.5pt;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8c734b;
    font-weight: 600;
    margin-bottom: 5px;
  }

  .brand-tagline {
    font-family: 'Georgia', serif;
    font-size: 9.5pt;
    font-style: italic;
    color: #4a4a4a;
    margin-bottom: 5px;
  }

  .brand-desc {
    font-size: 7.8pt;
    color: #555555;
    max-width: 95%;
    margin: 0 auto;
    line-height: 1.3;
  }

  /* Market Expansion Banner */
  .market-banner {
    background: linear-gradient(135deg, #1f2836 0%, #111622 100%);
    color: #ffffff;
    text-align: center;
    padding: 6px 10px;
    border-radius: 3px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-size: 8.5pt;
    font-weight: bold;
    border: 1px solid #000000;
  }

  .market-banner span {
    color: #d4af37;
  }

  /* Section Titles */
  .section-header {
    font-family: 'Georgia', serif;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #1f2836;
    border-bottom: 1.5px solid #8c734b;
    padding-bottom: 3px;
    margin-bottom: 8px;
    font-weight: bold;
  }

  /* Product Catalog Table */
  .products-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 5px;
    margin-bottom: 10px;
  }

  .product-card {
    background: #ffffff;
    border: 1px solid #e1dbd0;
    border-radius: 4px;
    padding: 7px 5px;
    text-align: center;
    vertical-align: top;
    width: 20%;
  }

  .product-icon-container {
    height: 42px;
    display: block;
    margin: 0 auto 4px auto;
  }

  .product-name {
    font-size: 7.8pt;
    font-weight: bold;
    color: #1a1a1a;
    height: 24px;
    line-height: 1.15;
    margin-bottom: 5px;
    display: block;
  }

  .price-box {
    background: #f5f2eb;
    border-radius: 3px;
    padding: 4px 2px;
    border: 1px solid #ebd3c2;
  }

  .price-public {
    font-size: 7pt;
    color: #555;
  }

  .price-public span {
    font-weight: bold;
    color: #1a1a1a;
  }

  .price-gros {
    font-size: 8.2pt;
    color: #8c734b;
    font-weight: bold;
    margin-top: 2px;
  }

  /* Main Layout Grid */
  .main-grid {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
  }

  .grid-col-left {
    width: 49%;
    vertical-align: top;
    padding-right: 7px;
  }

  .grid-col-right {
    width: 51%;
    vertical-align: top;
    padding-left: 7px;
  }

  /* Info Card Box */
  .card-box {
    background: #ffffff;
    border: 1px solid #e1dbd0;
    border-radius: 4px;
    padding: 8px 10px;
    margin-bottom: 8px;
  }

  .card-box-title {
    font-family: 'Georgia', serif;
    font-size: 8.5pt;
    font-weight: bold;
    color: #8c734b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 5px;
    border-bottom: 1px dashed #e1dbd0;
    padding-bottom: 3px;
  }

  .spec-table {
    width: 100%;
    border-collapse: collapse;
  }

  .spec-table td {
    padding: 2px 0;
    vertical-align: top;
    font-size: 7.8pt;
  }

  .spec-label {
    font-weight: bold;
    color: #2c2c2c;
    width: 42%;
  }

  .spec-value {
    color: #4a4a4a;
  }

  /* Financial Simulation Callout */
  .finance-box {
    background: #f7f4ed;
    border: 1px solid #dcd3c3;
    border-radius: 4px;
    padding: 8px 10px;
    margin-bottom: 8px;
  }

  .finance-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 5px;
  }

  .finance-cell {
    width: 33.33%;
    text-align: center;
    border-right: 1px solid #dcd3c3;
    padding: 3px 2px;
  }

  .finance-cell:last-child {
    border-right: none;
  }

  .finance-lbl {
    font-size: 6.8pt;
    text-transform: uppercase;
    color: #666;
    letter-spacing: 0.3px;
  }

  .finance-val {
    font-size: 9.5pt;
    font-weight: bold;
    color: #1f2836;
    margin-top: 2px;
  }

  .finance-val.accent {
    color: #8c734b;
  }

  /* Highlight Swiss Experience */
  .swiss-exp-box {
    background: #f0f4f8;
    border-left: 3.5px solid #1f2836;
    border-top: 1px solid #e1e6ed;
    border-right: 1px solid #e1e6ed;
    border-bottom: 1px solid #e1e6ed;
    padding: 8px 10px;
    border-radius: 0 4px 4px 0;
    margin-bottom: 8px;
  }

  .swiss-exp-title {
    font-family: 'Georgia', serif;
    font-size: 8.5pt;
    font-weight: bold;
    color: #1f2836;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .swiss-exp-text {
    font-size: 7.6pt;
    color: #333333;
    line-height: 1.35;
  }

  .swiss-exp-text strong {
    color: #1f2836;
  }

  /* Lists */
  .bullet-list {
    list-style: none;
    padding-left: 0;
  }

  .bullet-list li {
    position: relative;
    padding-left: 11px;
    margin-bottom: 3.5px;
    font-size: 7.6pt;
    color: #333333;
    line-height: 1.3;
  }

  .bullet-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #8c734b;
    font-weight: bold;
    font-size: 9pt;
  }

  /* Call to Action Box */
  .cta-box {
    background: #1f2836;
    color: #ffffff;
    border-radius: 4px;
    padding: 8px 12px;
    text-align: center;
    margin-bottom: 8px;
  }

  .cta-title {
    font-family: 'Georgia', serif;
    font-size: 9.5pt;
    font-weight: bold;
    color: #d4af37;
    margin-bottom: 3px;
    letter-spacing: 0.5px;
  }

  .cta-desc {
    font-size: 7.8pt;
    color: #e2e8f0;
    line-height: 1.3;
  }

  /* Footer Section */
  .footer-container {
    border-top: 1px solid #d8d2c7;
    padding-top: 6px;
    text-align: center;
  }

  .footer-contacts {
    font-size: 7.8pt;
    color: #2c2c2c;
    margin-bottom: 3px;
  }

  .footer-contacts span.sep {
    color: #8c734b;
    margin: 0 6px;
    font-weight: bold;
  }

  .footer-company {
    font-size: 7.2pt;
    color: #666;
    margin-bottom: 4px;
  }

  .footer-disclaimer {
    font-size: 6.2pt;
    color: #888888;
    line-height: 1.2;
    max-width: 98%;
    margin: 0 auto;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header-container">
    <div class="swiss-badge">Marque Suisse Fondée en 2011</div>
    <div class="brand-logo">NATKINA</div>
    <div class="brand-location">GENÈVE &bull; MONTREUX</div>
    <div class="brand-tagline">&laquo; L'argent que l'on porte tous les jours. &raquo;</div>
    <div class="brand-desc">
      Bijouterie fine en Argent sterling 925 rhodié et zircons sertis main. Marque familiale basée à Montreux, dirigée par des femmes.
    </div>
  </div>

  <!-- Market Expansion Banner -->
  <div class="market-banner">
    VENTE EN GROS FRANCE &mdash; <span>Développement du Réseau de Partenaires</span>
  </div>

  <!-- Bestsellers Section -->
  <div class="section-header">Sélection Best-Sellers (Tarif Pro France en €)</div>
  <table class="products-table">
    <tr>
      <!-- Product 1 -->
      <td class="product-card">
        <svg class="product-icon-container" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="20" cy="20" r="11" stroke="#8c734b" stroke-width="1.2" fill="#fdfbf7"/>
          <circle cx="20" cy="20" r="5" fill="#8c734b" opacity="0.3"/>
          <path d="M20 9 L20 31 M9 20 L31 20" stroke="#8c734b" stroke-width="0.7" stroke-dasharray="2 1"/>
        </svg>
        <div class="product-name">Classic Round Studs</div>
        <div class="price-box">
          <div class="price-public">Prix Public : <span>149 €</span></div>
          <div class="price-gros">Gros : 50 €</div>
        </div>
      </td>

      <!-- Product 2 -->
      <td class="product-card">
        <svg class="product-icon-container" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="11" y="11" width="18" height="18" rx="4" stroke="#8c734b" stroke-width="1.2" fill="#fdfbf7"/>
          <polygon points="20,13 25,20 20,27 15,20" fill="#8c734b" opacity="0.35"/>
        </svg>
        <div class="product-name">Cushion Cut Karolina Ring</div>
        <div class="price-box">
          <div class="price-public">Prix Public : <span>249 €</span></div>
          <div class="price-gros">Gros : 83 €</div>
        </div>
      </td>

      <!-- Product 3 -->
      <td class="product-card">
        <svg class="product-icon-container" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 20 C11 11, 29 11, 33 20 C29 29, 11 29, 7 20 Z" stroke="#8c734b" stroke-width="1.2" fill="#fdfbf7"/>
          <circle cx="13" cy="20" r="2" fill="#8c734b"/>
          <circle cx="20" cy="20" r="2.5" fill="#8c734b"/>
          <circle cx="27" cy="20" r="2" fill="#8c734b"/>
        </svg>
        <div class="product-name">Classic Silver Tennis Bracelet</div>
        <div class="price-box">
          <div class="price-public">Prix Public : <span>322 €</span></div>
          <div class="price-gros">Gros : 107 €</div>
        </div>
      </td>

      <!-- Product 4 -->
      <td class="product-card">
        <svg class="product-icon-container" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 7 L20 18 M14 18 C14 25, 26 25, 26 18 C26 12, 14 12, 14 18" stroke="#8c734b" stroke-width="1.2" fill="none"/>
          <rect x="15" y="20" width="10" height="10" stroke="#8c734b" stroke-width="1" fill="#fdfbf7"/>
        </svg>
        <div class="product-name">Square Leverback Earrings</div>
        <div class="price-box">
          <div class="price-public">Prix Public : <span>217 €</span></div>
          <div class="price-gros">Gros : 72 €</div>
        </div>
      </td>

      <!-- Product 5 -->
      <td class="product-card">
        <svg class="product-icon-container" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 28 L13 21 C9 17, 11 11, 16 11 C18.5 11, 20 13, 20 13 C20 13, 21.5 11, 24 11 C29 11, 31 17, 27 21 Z" stroke="#8c734b" stroke-width="1.2" fill="#fdfbf7"/>
        </svg>
        <div class="product-name">Enchanted Heart Ring</div>
        <div class="price-box">
          <div class="price-public">Prix Public : <span>148 €</span></div>
          <div class="price-gros">Gros : 49 €</div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Main Content Columns Grid -->
  <table class="main-grid">
    <tr>
      <!-- Column Left -->
      <td class="grid-col-left">

        <!-- Conditions Commerciales -->
        <div class="card-box">
          <div class="card-box-title">Conditions Commerciales</div>
          <table class="spec-table">
            <tr>
              <td class="spec-label">Assortiment :</td>
              <td class="spec-value">Bagues, Boucles d'oreilles, Colliers, Bracelets</td>
            </tr>
            <tr>
              <td class="spec-label">Gamme de prix :</td>
              <td class="spec-value"><strong>119 € &ndash; 440 €</strong> (Prix public conseillé TTC)</td>
            </tr>
            <tr>
              <td class="spec-label">Tailles bagues :</td>
              <td class="spec-value">48 à 60</td>
            </tr>
            <tr>
              <td class="spec-label">Votre marge :</td>
              <td class="spec-value"><strong>Coeff. x3</strong> (Prix de gros = 1/3 prix public TTC)</td>
            </tr>
            <tr>
              <td class="spec-label">Composition :</td>
              <td class="spec-value">Libre choix, aucun minimum par modèle</td>
            </tr>
          </table>
        </div>

        <!-- Simulation Commande Initial -->
        <div class="finance-box">
          <div class="card-box-title" style="border:none; margin-bottom: 2px; padding-bottom: 0;">Exemple d'Assortiment Initial</div>
          <div style="font-size: 7.2pt; color: #555; margin-bottom: 4px;">
            Sélection de <strong>53 pièces</strong> optimisée d'après 24 mois de ventes réelles :
          </div>
          <table class="finance-table">
            <tr>
              <td class="finance-cell">
                <div class="finance-lbl">Investissement</div>
                <div class="finance-val">3 000 €</div>
              </td>
              <td class="finance-cell">
                <div class="finance-lbl">Valeur Vente TTC</div>
                <div class="finance-val">9 000 €</div>
              </td>
              <td class="finance-cell">
                <div class="finance-lbl">Marge Brute</div>
                <div class="finance-val accent">6 000 €</div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Protection & Sécurité Partenaire -->
        <div class="card-box">
          <div class="card-box-title">Engagements & Services</div>
          <ul class="bullet-list">
            <li><strong>Risque maîtrisé :</strong> Échange possible jusqu'à 20% de la commande si un modèle ne part pas (modalités selon accord).</li>
            <li><strong>Livraison rapide :</strong> Expédition sous 2 semaines en règle générale (dans la limite des stocks disponibles).</li>
            <li><strong>Packaging offert :</strong> Écrin et emballage de marque inclus sans supplément pour chaque pièce.</li>
            <li><strong>Garantie 2 ans :</strong> Service après-vente et prise en charge directe par nos soins.</li>
          </ul>
        </div>

      </td>

      <!-- Column Right -->
      <td class="grid-col-right">

        <!-- Expérience Suisse & Expansion France -->
        <div class="swiss-exp-box">
          <div class="swiss-exp-title">Savoir-Faire Suisse & Expansion France</div>
          <div class="swiss-exp-text">
            <strong>Une expérience éprouvée sur le marché suisse :</strong><br>
            Durant 4 ans, NATKINA a développé sa présence en propre dans des grands magasins d'exception en Suisse : <strong>Globus Genève</strong>, <strong>Globus Gstaad</strong> et <strong>Jelmoli Zurich</strong> (jusqu'au début 2025).<br><br>
            Nos données de caisse confirment un fort engouement client : <strong>panier moyen de 244 €</strong> et <strong>187 pièces vendues/mois</strong> à Zurich en moyenne.<br><br>
            Forts de ce succès et de notre solide expérience, nous développons aujourd'hui notre réseau de boutiques partenaires en <strong>France</strong>.
          </div>
        </div>

        <!-- Territoire Exclusif -->
        <div class="card-box">
          <div class="card-box-title">Exclusivité Territoriale</div>
          <ul class="bullet-list">
            <li><strong>Zone réservée :</strong> Un seul partenaire par secteur géographique, consigné par écrit dans l'accord.</li>
            <li><strong>Conditions d'implantation :</strong> Souplesse accordée durant la phase initiale d'attribution des zones en France.</li>
          </ul>
        </div>

        <!-- Support Vente & Marketing -->
        <div class="card-box">
          <div class="card-box-title">Accompagnement Commercial</div>
          <ul class="bullet-list">
            <li><strong>Visibilité :</strong> Référencement de votre boutique sur <em>natkina.com</em> & publication dédiée sur Instagram (@natkina).</li>
            <li><strong>Supports marketing :</strong> Banque de visuels HD fournie pour vos vitrines et réseaux sociaux.</li>
            <li><strong>Données de vente :</strong> Partage du détail des ventes par modèle pour optimiser la rotation de votre stock.</li>
          </ul>
        </div>

      </td>
    </tr>
  </table>

  <!-- Call to Action -->
  <div class="cta-box">
    <div class="cta-title">15 minutes suffisent pour lancer votre partenariat</div>
    <div class="cta-desc">
      Rencontrez <strong>Martina Netovkina</strong> (fondatrice & dirigeante) en visioconférence ou planifions une visite dans votre boutique avec la valise d'échantillons.
    </div>
  </div>

  <!-- Footer -->
  <div class="footer-container">
    <div class="footer-contacts">
      Email : <strong>admin@natkina.com</strong>
      <span class="sep">&bull;</span>
      Site web : <strong>natkina.com</strong>
      <span class="sep">&bull;</span>
      Instagram : <strong>@natkina</strong>
    </div>
    <div class="footer-company">
      <strong>NATKINA Jewellery Office SA</strong> &mdash; Montreux, Suisse
    </div>
    <div class="footer-disclaimer">
      Document d'information sans valeur contractuelle. Seuls le tarif professionnel et l'accord de partenariat font foi. Chiffres issus de nos ventes directes en propre en Suisse, fournis à titre indicatif sans garantie de chiffre d'affaires pour votre point de vente.
    </div>
  </div>

</body>
</html>
"""

output_filename = "NATKINA_Onepager_FR_v5.pdf"
HTML(string=html_content).write_pdf(output_filename)

doc = pypdf.PdfReader(output_filename)
print("Total pages in v5:", len(doc.pages))