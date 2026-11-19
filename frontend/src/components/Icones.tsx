import type { SVGProps } from "react";

type Props = SVGProps<SVGSVGElement> & { tamanho?: number };

function Base({ tamanho = 18, children, ...resto }: Props) {
  return (
    <svg
      width={tamanho}
      height={tamanho}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...resto}
    >
      {children}
    </svg>
  );
}

export const IconeMais = (p: Props) => (
  <Base {...p}><path d="M12 5v14M5 12h14" /></Base>
);
export const IconeBusca = (p: Props) => (
  <Base {...p}><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></Base>
);
export const IconeAlvo = (p: Props) => (
  <Base {...p}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.5" /></Base>
);
export const IconePasta = (p: Props) => (
  <Base {...p}><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /></Base>
);
export const IconeRobo = (p: Props) => (
  <Base {...p}><rect x="4" y="8" width="16" height="11" rx="3" /><path d="M12 4v4M9 13h.01M15 13h.01" /></Base>
);
export const IconePessoa = (p: Props) => (
  <Base {...p}><circle cx="12" cy="8" r="4" /><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6" /></Base>
);
export const IconeBaixar = (p: Props) => (
  <Base {...p}><path d="M12 4v11m0 0-4-4m4 4 4-4M5 20h14" /></Base>
);
export const IconeOlho = (p: Props) => (
  <Base {...p}><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></Base>
);
export const IconeOlhoRiscado = (p: Props) => (
  <Base {...p}><path d="M3 3l18 18M10.6 6.1A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3.2 3.9M6.5 7.5A17 17 0 0 0 2 12s3.5 7 10 7a9.6 9.6 0 0 0 4-.9" /></Base>
);
export const IconeFechar = (p: Props) => (
  <Base {...p}><path d="M6 6l12 12M18 6 6 18" /></Base>
);
export const IconeSeta = (p: Props) => (
  <Base {...p}><path d="M5 12h14m0 0-5-5m5 5-5 5" /></Base>
);
export const IconeCheck = (p: Props) => (
  <Base {...p}><path d="m5 12.5 4.5 4.5L19 7.5" /></Base>
);
export const IconeCirculoCheck = (p: Props) => (
  <Base {...p}><circle cx="12" cy="12" r="9" /><path d="m8 12.5 3 3 5-6" /></Base>
);
export const IconeSinal = (p: Props) => (
  <Base {...p}><path d="M5 19v-4M10 19v-8M15 19V7M20 19V3" /></Base>
);
export const IconeInterrogacao = (p: Props) => (
  <Base {...p}><circle cx="12" cy="12" r="9" /><path d="M9.5 9.5a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1.9-1.1 1.8M12 17h.01" /></Base>
);
export const IconeTracejado = (p: Props) => (
  <Base {...p}><circle cx="12" cy="12" r="9" strokeDasharray="3 3" /></Base>
);
export const IconeAlerta = (p: Props) => (
  <Base {...p}><path d="M12 3 2 20h20z" /><path d="M12 10v4M12 17h.01" /></Base>
);
export const IconeEscudo = (p: Props) => (
  <Base {...p}><path d="M12 3 4 6v6c0 4.5 3.2 7.8 8 9 4.8-1.2 8-4.5 8-9V6z" /><path d="m9 12 2 2 4-4" /></Base>
);
export const IconeRelogio = (p: Props) => (
  <Base {...p}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></Base>
);
export const IconeCartao = (p: Props) => (
  <Base {...p}><rect x="3" y="5" width="18" height="14" rx="2" /><path d="M3 10h18" /></Base>
);
export const IconeSair = (p: Props) => (
  <Base {...p}><path d="M10 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h4M15 8l4 4-4 4M19 12H9" /></Base>
);

export function Logo({ tamanho = 36 }: { tamanho?: number }) {
  return (
    <svg width={tamanho} height={tamanho} viewBox="0 0 32 32" aria-hidden="true">
      <rect width="32" height="32" rx="7" fill="#00685f" />
      <circle cx="16" cy="16" r="8" fill="none" stroke="#fff" strokeWidth="2.4" />
      <circle cx="16" cy="16" r="3" fill="#fff" />
    </svg>
  );
}
