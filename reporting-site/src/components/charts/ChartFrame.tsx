import type { ReactNode } from "react";
import { C, FONT_MONO } from "../../lib/charts/tokens";

/**
 * ChartFrame — shared editorial chrome for a native chart.
 *
 * Renders the title / subtitle / one big headline number / source +
 * attestation footer. Crucially the `attestation_chain` is rendered as
 * real, selectable text (not burned into pixels like the PNG path). That
 * keeps §18.2 honest-labeling satisfied in the native rendering: the
 * label travels with the figure and is even copy-pasteable.
 */
export interface ChartFrameProps {
  kicker?: string;
  title: string;
  subtitle?: string;
  headline?: { value: string; label?: string };
  source: string;
  attestation?: string;
  program?: string;
  note?: ReactNode;
  children: ReactNode;
}

export function ChartFrame({
  kicker,
  title,
  subtitle,
  headline,
  source,
  attestation = "ai-first",
  program,
  note,
  children,
}: ChartFrameProps) {
  return (
    <figure
      style={{
        margin: 0,
        background: C.paper,
        border: `1px solid ${C.ruleSoft}`,
        borderRadius: 10,
        padding: "clamp(16px, 2.4vw, 28px)",
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: 16,
          marginBottom: 14,
        }}
      >
        <div style={{ flex: "1 1 280px", minWidth: 0 }}>
          {kicker && (
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 11,
                textTransform: "uppercase",
                letterSpacing: "0.16em",
                color: C.accentStrong,
                marginBottom: 7,
              }}
            >
              {kicker}
            </div>
          )}
          <h3
            style={{
              margin: 0,
              fontSize: "clamp(1.2rem, 2.4vw, 1.6rem)",
              fontWeight: 700,
              lineHeight: 1.18,
              color: C.ink,
              letterSpacing: "-0.01em",
            }}
          >
            {title}
          </h3>
          {subtitle && (
            <p
              style={{
                margin: "8px 0 0",
                fontSize: "0.95rem",
                lineHeight: 1.45,
                color: C.inkSoft,
                maxWidth: "62ch",
              }}
            >
              {subtitle}
            </p>
          )}
        </div>
        {headline && (
          <div style={{ flex: "0 0 auto", textAlign: "right" }}>
            <div
              style={{
                fontFamily: FONT_MONO,
                fontWeight: 700,
                fontSize: "clamp(1.9rem, 5vw, 2.9rem)",
                lineHeight: 1,
                color: C.ink,
                letterSpacing: "-0.02em",
              }}
            >
              {headline.value}
            </div>
            {headline.label && (
              <div
                style={{
                  marginTop: 6,
                  fontSize: 12,
                  color: C.inkFaint,
                  maxWidth: 200,
                  marginLeft: "auto",
                }}
              >
                {headline.label}
              </div>
            )}
          </div>
        )}
      </div>

      {children}

      {note && (
        <div
          style={{
            marginTop: 12,
            fontSize: 12.5,
            lineHeight: 1.45,
            color: C.inkSoft,
            borderLeft: `3px solid ${C.ochre}`,
            paddingLeft: 10,
          }}
        >
          {note}
        </div>
      )}

      <figcaption
        style={{
          marginTop: 14,
          paddingTop: 10,
          borderTop: `1px solid ${C.ruleSoft}`,
          display: "flex",
          flexWrap: "wrap",
          gap: "4px 10px",
          fontFamily: FONT_MONO,
          fontSize: 11,
          color: C.inkFaint,
        }}
      >
        <span>Source: {source}</span>
        <span aria-hidden>·</span>
        <span>
          attestation_chain:{" "}
          <span style={{ color: C.accentStrong }}>{attestation}</span>
        </span>
        {program && (
          <>
            <span aria-hidden>·</span>
            <span>{program}</span>
          </>
        )}
      </figcaption>
    </figure>
  );
}
