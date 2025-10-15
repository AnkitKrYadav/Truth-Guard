import React from "react";
import { AiOutlineSafetyCertificate } from "react-icons/ai";

const Header = () => {
  return (
    <header className="site-header" role="banner">
      <div className="site-header-inner container">
        <div className="brand">
          <AiOutlineSafetyCertificate className="brand-icon" />
          <div>
            <h1 className="brand-title">TruthGuard</h1>
            <p className="brand-sub">Your AI Shield Against Digital Deception</p>
          </div>
        </div>

        <nav className="main-nav" aria-label="Main navigation">
          <a href="#how" className="nav-link">How it works</a>
          <a href="#demo" className="nav-link">Demo</a>
          <a href="#team" className="nav-link">Team</a>
        </nav>
      </div>
    </header>
  );
};

export default Header;
