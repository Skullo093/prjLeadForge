import type { ReactNode } from "react";
import { IconeAlerta, IconeCirculoCheck, IconeFechar } from "./Icones";

interface Props {
  tipo: "ok" | "erro" | "info";
  titulo?: string;
  children?: ReactNode;
  aoFechar?: () => void;
}

export function Alerta({ tipo, titulo, children, aoFechar }: Props) {
  return (
    <div className={`alerta alerta-${tipo}`} role={tipo === "erro" ? "alert" : "status"}>
      {tipo === "erro" ? <IconeAlerta /> : <IconeCirculoCheck />}
      <div>
        {titulo && <strong>{titulo}</strong>}
        {children}
      </div>
      {aoFechar && (
        <button className="fechar" onClick={aoFechar} aria-label="Fechar aviso">
          <IconeFechar />
        </button>
      )}
    </div>
  );
}
