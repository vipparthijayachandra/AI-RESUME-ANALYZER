"""ResumeIQ visual theme and dashboard styling."""

import streamlit as st


def load_custom_css() -> None:
    """Apply the ResumeIQ premium dashboard theme."""

    st.markdown(
        """
        <style>

        /* =========================================
           GLOBAL
        ========================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(67, 117, 255, 0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 8%,
                    rgba(124, 58, 237, 0.10),
                    transparent 30%
                ),
                #ffffff;
        }

        .main .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }


        /* =========================================
           HERO
        ========================================= */

        .resumeiq-hero {
            min-height: 520px;

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 70px;

            padding: 55px 10px 65px 10px;
        }


        .hero-left {
            flex: 1;
            max-width: 650px;
        }


        /* =========================================
           BADGE
        ========================================= */

        .resumeiq-badge {
            display: inline-flex;
            align-items: center;

            padding: 9px 16px;

            border-radius: 999px;

            background: rgba(37, 99, 235, 0.07);

            border: 1px solid rgba(37, 99, 235, 0.18);

            color: #2563eb;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.8px;

            margin-bottom: 20px;
        }


        /* =========================================
           TITLE
        ========================================= */

        .resumeiq-title {
            margin: 0;

            font-size: clamp(62px, 7vw, 92px);

            line-height: 0.95;

            font-weight: 850;

            letter-spacing: -5px;

            color: #111827;
        }


        .resumeiq-title span {
            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #7c3aed
                );

            -webkit-background-clip: text;
            background-clip: text;

            -webkit-text-fill-color: transparent;
        }


        /* =========================================
           SUBTITLE
        ========================================= */

        .resumeiq-subtitle {
            max-width: 620px;

            margin-top: 25px;

            font-size: 20px;

            line-height: 1.65;

            color: #667085;
        }


        /* =========================================
           HERO POINTS
        ========================================= */

        .hero-points {
            display: flex;

            flex-wrap: wrap;

            gap: 14px;

            margin-top: 28px;
        }


        .hero-point {
            display: flex;

            align-items: center;

            gap: 7px;

            color: #475467;

            font-size: 14px;

            font-weight: 600;
        }


        .hero-point span {
            width: 22px;
            height: 22px;

            display: inline-flex;

            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background: #e8f7ef;

            color: #12a66a;

            font-size: 12px;

            font-weight: 800;
        }


        /* =========================================
           HERO VISUAL
        ========================================= */

        .hero-visual {
            position: relative;

            width: 490px;

            min-width: 490px;

            min-height: 430px;

            display: flex;

            align-items: center;

            justify-content: center;
        }


        /* =========================================
           RESUME WINDOW
        ========================================= */

        .resume-preview {
            width: 400px;

            min-height: 340px;

            background: rgba(255,255,255,0.92);

            border: 1px solid #e5e7eb;

            border-radius: 22px;

            box-shadow:
                0 25px 70px rgba(15,23,42,0.13);

            overflow: hidden;

            transform: rotate(1deg);

            animation: resumeFloat 4s ease-in-out infinite;
        }


        .resume-window-top {
            height: 42px;

            display: flex;

            align-items: center;

            gap: 7px;

            padding-left: 18px;

            background: #f8fafc;

            border-bottom: 1px solid #eef2f6;
        }


        .window-dot {
            width: 9px;
            height: 9px;

            border-radius: 50%;

            background: #d0d5dd;
        }


        .resume-content {
            padding: 27px;
        }


        .resume-header-row {
            display: flex;

            align-items: flex-start;

            justify-content: space-between;
        }


        .resume-name {
            font-size: 22px;

            font-weight: 800;

            color: #101828;
        }


        .resume-role {
            margin-top: 4px;

            font-size: 12px;

            color: #667085;
        }


        /* =========================================
           ATS CIRCLE
        ========================================= */

        .ats-circle {
            width: 76px;
            height: 76px;

            border-radius: 50%;

            display: flex;

            flex-direction: column;

            align-items: center;

            justify-content: center;

            background:
                radial-gradient(
                    circle,
                    #ffffff 57%,
                    transparent 58%
                );

            border: 7px solid #10b981;

            box-shadow:
                0 8px 25px rgba(16,185,129,0.18);
        }


        .ats-number {
            font-size: 20px;

            font-weight: 850;

            color: #101828;

            line-height: 1;
        }


        .ats-label {
            margin-top: 3px;

            font-size: 8px;

            font-weight: 800;

            letter-spacing: 0.5px;

            color: #12a66a;
        }


        /* =========================================
           RESUME LINES
        ========================================= */

        .resume-line {
            height: 8px;

            border-radius: 999px;

            background: #eef2f6;

            margin-top: 9px;
        }


        .resume-line.long {
            width: 85%;
        }


        .resume-line.medium {
            width: 65%;
        }


        .resume-line.short {
            width: 42%;
        }


        .resume-section-title {
            margin-top: 24px;

            font-size: 9px;

            font-weight: 850;

            letter-spacing: 1px;

            color: #2563eb;
        }


        /* =========================================
           SKILLS
        ========================================= */

        .skill-row {
            display: flex;

            flex-wrap: wrap;

            gap: 6px;

            margin-top: 12px;
        }


        .skill-row span {
            padding: 6px 9px;

            border-radius: 7px;

            background: #eef4ff;

            color: #2563eb;

            font-size: 9px;

            font-weight: 700;
        }


        /* =========================================
           FLOATING CARDS
        ========================================= */

        .floating-card {
            position: absolute;

            background: rgba(255,255,255,0.95);

            border: 1px solid #e5e7eb;

            border-radius: 15px;

            box-shadow:
                0 15px 40px rgba(15,23,42,0.10);

            padding: 13px 17px;

            z-index: 5;
        }


        .floating-card-top {
            top: 40px;

            right: 5px;

            display: flex;

            align-items: center;

            gap: 9px;

            font-size: 12px;

            color: #475467;

            animation: floatingTop 3.5s ease-in-out infinite;
        }


        .floating-card-top strong {
            color: #12a66a;
        }


        .floating-icon {
            color: #7c3aed;

            font-size: 17px;
        }


        .floating-card-bottom {
            bottom: 35px;

            left: 10px;

            display: flex;

            align-items: center;

            gap: 10px;

            animation: floatingBottom 4s ease-in-out infinite;
        }


        .floating-card-bottom small {
            display: block;

            font-size: 10px;

            color: #98a2b3;
        }


        .floating-card-bottom strong {
            display: block;

            margin-top: 2px;

            color: #101828;

            font-size: 12px;
        }


        .check-icon {
            width: 30px;
            height: 30px;

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 50%;

            background: #e8f7ef;

            color: #12a66a;

            font-weight: 800;
        }


        /* =========================================
           ANIMATIONS
        ========================================= */

        @keyframes resumeFloat {

            0%,
            100% {
                transform: translateY(0) rotate(1deg);
            }

            50% {
                transform: translateY(-9px) rotate(1deg);
            }
        }


        @keyframes floatingTop {

            0%,
            100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-7px);
            }
        }


        @keyframes floatingBottom {

            0%,
            100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(7px);
            }
        }


        /* =========================================
           STREAMLIT CARDS
        ========================================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px !important;

            border: 1px solid #e5e7eb !important;

            background: rgba(255,255,255,0.86) !important;

            box-shadow:
                0 8px 30px rgba(15,23,42,0.05) !important;
        }


        /* =========================================
           UPLOAD AREA
        ========================================= */

        section[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #8bb5ff !important;

            border-radius: 18px !important;

            background: #f8fbff !important;

            padding: 12px !important;
        }


        section[data-testid="stFileUploaderDropzone"]:hover {
            background: #f1f6ff !important;

            border-color: #4d83ff !important;
        }


        /* =========================================
           BUTTONS
        ========================================= */

        .stButton > button {
            border-radius: 12px !important;

            border: none !important;

            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #4f46e5
                ) !important;

            color: white !important;

            font-weight: 700 !important;

            padding: 0.7rem 1.25rem !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        .stButton > button:hover {
            transform: translateY(-2px);

            box-shadow:
                0 10px 25px rgba(37,99,235,0.25);
        }


        /* =========================================
           ALERTS
        ========================================= */

        div[data-testid="stAlert"] {
            border-radius: 14px !important;

            border: 1px solid rgba(37,99,235,0.12) !important;
        }


        /* =========================================
           HEADINGS
        ========================================= */

        h1,
        h2,
        h3 {
            color: #111827 !important;
        }


        h2 {
            font-size: 30px !important;

            font-weight: 750 !important;
        }


        h3 {
            font-size: 22px !important;
        }


        /* =========================================
           METRICS
        ========================================= */

        div[data-testid="stMetric"] {
            background: #ffffff;

            border: 1px solid #e5e7eb;

            border-radius: 16px;

            padding: 18px;

            box-shadow:
                0 5px 20px rgba(15,23,42,0.04);
        }


        div[data-testid="stMetricLabel"] {
            color: #667085 !important;
        }


        div[data-testid="stMetricValue"] {
            color: #111827 !important;

            font-weight: 750 !important;
        }


        /* =========================================
           MOBILE
        ========================================= */

        @media (max-width: 900px) {

            .resumeiq-hero {
                flex-direction: column;

                align-items: flex-start;

                gap: 30px;
            }

            .hero-visual {
                width: 100%;

                min-width: 0;

                transform: scale(0.92);

                transform-origin: left top;
            }

        }


        @media (max-width: 600px) {

            .main .block-container {
                padding-left: 1rem;

                padding-right: 1rem;
            }

            .resumeiq-title {
                font-size: 58px;

                letter-spacing: -3px;
            }

            .resumeiq-subtitle {
                font-size: 17px;
            }

            .resume-preview {
                width: 330px;
            }

            .hero-visual {
                min-height: 380px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )