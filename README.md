# GoNano Competitor Intelligence Tool — Certified Contractor Portal

A field-ready competitive intelligence and market reconnaissance platform tailored specifically for **GoNano Certified Applicators & Contractors**.

---

## Key Features

1. **Competitor Analysis Request Portal (Tab 1):**
   * Certified contractors can submit unmonitored competitors encountered in the field.
   * **Required & Optional Fields:** Competitor Name, Market Location, Website URL, Facebook Page, Instagram Handle, Contractor Info, and Field Notes.
   * **Screenshot / Evidence Upload:** Multi-file uploader for quotes, flyers, warranty certificates, and social ads.
   * **Direct Routing:** Requests and attached evidence are dispatched headlessly via SMTP directly to **`miguel.gonzales@gonano.com`**.
   * **Local Persistence:** Preserves inquiry history in the embedded SQLite database.

2. **Sales Battlecards & Objection Playbooks (Tab 2):**
   * Tactical counter-arguments, pricing anchors, and fact-checked scientific rebuttals contrasting GoNano against rival formulations (RoofLife Canada, Roof Maxx, RevivaRoof, Nasiol, Spray-Net, etc.).

3. **Empirical Head-to-Head Comparative Scorecards (Tab 3):**
   * Side-by-side technical benchmarks with verified citations covering chemistry, durability, hail/wind resistance, and cost-per-square-foot.

4. **Technical ASTM Formulation Lab (Tab 8):**
   * Independent ASTM D3462 nail tear strength, ASTM D3161 wind uplift, and UL 2218 Class 4 hail impact teardowns proving the structural superiority of GoNano's covalent silica matrix over perishable bio-oils.

5. **Purely In-Memory Search (No Background Updates):**
   * Contains zero automated C-suite email schedulers or broadcast functions.
   * Standalone desktop execution via native launcher.

---

## Local Launching

Double-click the desktop launcher:
```bash
./run_native_app.sh
```
Or run directly with Streamlit:
```bash
streamlit run app.py --server.port 8503
```
