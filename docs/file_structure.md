
## Project file structure (refreshed)

This document contains a complete, up-to-date listing of the repository structure as an ASCII tree and a Mermaid diagram. Use the Mermaid block below in mermaid.live or a VS Code Mermaid preview to render a visual.

### ASCII tree

Truth-Guard/
├─ .gitattributes
├─ .gitignore
├─ README.md
├─ Backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ news.db
│  ├─ routes/
│  │  ├─ fetch_news.py
│  │  └─ verify_news.py
│  └─ utils/
│     ├─ fact_check.py
│     ├─ langchain_agent.py
│     └─ news_api.py
├─ database/
│  ├─ connection.py
│  ├─ database.py
│  └─ news.db
├─ docs/
│  └─ file_structure.md
└─ Frontend/
   └─ react-app/
      ├─ .gitignore
      ├─ package.json
      ├─ package-lock.json
      ├─ postcss.config.js
      ├─ tailwind.config.js
      ├─ README.md
      ├─ public/
      │  ├─ favicon.ico
      │  ├─ index.html
      │  ├─ manifest.json
      │  ├─ robots.txt
      │  ├─ logo192.png
      │  └─ logo512.png
      └─ src/
         ├─ App.css
         ├─ App.js
         ├─ App.test.js
         ├─ index.css
         ├─ index.js
         ├─ logo.svg
         ├─ reportWebVitals.js
         ├─ setupTests.js
         ├─ context/
         │  ├─ ThemeContext.jsx
         │  └─ UserPrefsContext.jsx
         ├─ pages/
         │  ├─ About.jsx
         │  ├─ Dashboard.jsx
         │  ├─ History.jsx
         │  ├─ Settings.jsx
         │  ├─ Trending.jsx
         │  └─ Verify.jsx
         └─ components/
            ├─ CustomizationPanel.jsx
            ├─ FactCard.jsx
            ├─ Header.jsx
            ├─ InputSection.jsx
            ├─ Navbar.jsx
            ├─ NewsCard.jsx
            ├─ Sidebar.jsx
            ├─ StatsWidget.jsx

### Mermaid diagram

Paste the block below into mermaid.live or a Mermaid preview to render and export the diagram.

```mermaid
graph TB
  subgraph Truth-Guard
    rootREADME["README.md"]
    rootGITIGNORE[".gitignore"]
    rootGITATTR[".gitattributes"]

    subgraph Backend
      B_app["app.py"]
      B_req["requirements.txt"]
      B_db["news.db"]
      subgraph routes
        B_fetch["fetch_news.py"]
        B_verify["verify_news.py"]
      end
      subgraph utils
        B_fact["fact_check.py"]
        B_lang["langchain_agent.py"]
        B_news["news_api.py"]
      end
    end

    subgraph database
      DB_conn["connection.py"]
      DB_db["news.db"]
      DB_dbpy["database.py"]
    end

    subgraph Frontend
      subgraph react-app
        F_git[".gitignore"]
        F_pkg["package.json"]
        F_pkglock["package-lock.json"]
        F_postcss["postcss.config.js"]
        F_tailwind["tailwind.config.js"]
        F_readme["README.md"]
        subgraph public
          P_fav["favicon.ico"]
          P_index["index.html"]
          P_manifest["manifest.json"]
          P_robots["robots.txt"]
          P_logo192["logo192.png"]
          P_logo512["logo512.png"]
        end
        subgraph src
          S_AppCss["App.css"]
          S_AppJs["App.js"]
          S_AppTest["App.test.js"]
          S_indexCss["index.css"]
          S_indexJs["index.js"]
          S_logo["logo.svg"]
          S_report["reportWebVitals.js"]
          S_setup["setupTests.js"]
          subgraph context
            C_theme["ThemeContext.jsx"]
            C_prefs["UserPrefsContext.jsx"]
          end
          subgraph pages
            P_about["About.jsx"]
            P_dashboard["Dashboard.jsx"]
            P_history["History.jsx"]
            P_settings["Settings.jsx"]
            P_trending["Trending.jsx"]
            P_verify["Verify.jsx"]
          end
          subgraph components
            C_custom["CustomizationPanel.jsx"]
            C_fact["FactCard.jsx"]
            C_header["Header.jsx"]
            C_input["InputSection.jsx"]
            C_nav["Navbar.jsx"]
            C_news["NewsCard.jsx"]
            C_sidebar["Sidebar.jsx"]
            C_stats["StatsWidget.jsx"]
          end
        end
      end
    end
  end
```

### How to use

- To render quickly: paste the Mermaid block into https://mermaid.live and export as PNG/SVG.
- In VS Code: install "Markdown Preview Mermaid Support" or "Mermaid Preview" and open this file.
- To include the rendered image in the repo: let me know and I'll generate a PNG/SVG and add `docs/structure.png`.

---

Refreshed on October 15, 2025.
