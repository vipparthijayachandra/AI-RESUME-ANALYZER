"""Reusable visual components for the ResumeIQ dashboard."""

import streamlit as st


def render_page_header() -> None:
    """Render the ResumeIQ hero section."""

    st.html(
        """
        <div class="resumeiq-hero">

            <div class="hero-left">

                <div class="resumeiq-badge">
                    ✦ &nbsp; AI-POWERED RESUME ANALYSIS
                </div>

                <h1 class="resumeiq-title">
                    Resume<span>IQ</span>
                </h1>

                <p class="resumeiq-subtitle">
                    Turn your resume into a stronger placement strategy.
                    Analyze your ATS score, discover matching roles,
                    and identify the skills you should develop next.
                </p>

                <div class="hero-points">
                    <div class="hero-point">
                        <span>✓</span>
                        ATS-style scoring
                    </div>

                    <div class="hero-point">
                        <span>✓</span>
                        Role matching
                    </div>

                    <div class="hero-point">
                        <span>✓</span>
                        Skill recommendations
                    </div>
                </div>

            </div>


            <div class="hero-visual">

                <div class="floating-card floating-card-top">
                    <span class="floating-icon">✦</span>
                    AI Analysis
                    <strong>Ready</strong>
                </div>


                <div class="resume-preview">

                    <div class="resume-window-top">
                        <div class="window-dot"></div>
                        <div class="window-dot"></div>
                        <div class="window-dot"></div>
                    </div>

                    <div class="resume-content">

                        <div class="resume-header-row">

                            <div>
                                <div class="resume-name">
                                    Your Resume
                                </div>

                                <div class="resume-role">
                                    Placement Candidate
                                </div>
                            </div>

                            <div class="ats-circle">
                                <div class="ats-number">91</div>
                                <div class="ats-label">ATS</div>
                            </div>

                        </div>


                        <div class="resume-line long"></div>
                        <div class="resume-line medium"></div>

                        <div class="resume-section-title">
                            EXPERIENCE
                        </div>

                        <div class="resume-line long"></div>
                        <div class="resume-line medium"></div>
                        <div class="resume-line short"></div>


                        <div class="resume-section-title">
                            SKILLS
                        </div>

                        <div class="skill-row">
                            <span>Python</span>
                            <span>Machine Learning</span>
                            <span>SQL</span>
                        </div>


                        <div class="resume-section-title">
                            EDUCATION
                        </div>

                        <div class="resume-line long"></div>
                        <div class="resume-line short"></div>

                    </div>

                </div>


                <div class="floating-card floating-card-bottom">
                    <span class="check-icon">✓</span>

                    <div>
                        <small>Profile Match</small>
                        <strong>Excellent</strong>
                    </div>
                </div>

            </div>

        </div>
        """
    )