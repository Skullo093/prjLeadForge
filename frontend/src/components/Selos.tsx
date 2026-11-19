import type { NivelCerteza, StatusContato } from "../api";
import {
  IconeCirculoCheck,
  IconeInterrogacao,
  IconeSinal,
  IconeTracejado,
} from "./Icones";

const NIVEIS: Record<NivelCerteza, { rotulo: string; Icone: typeof IconeSinal }> = {
  confirmado: { rotulo: "Confirmado", Icone: IconeCirculoCheck },
  sinal_forte: { rotulo: "Sinal forte", Icone: IconeSinal },
  inferencia: { rotulo: "Inferência", Icone: IconeInterrogacao },
  desconhecido: { rotulo: "Desconhecido", Icone: IconeTracejado },
};

export const ROTULO_NIVEL = Object.fromEntries(
  Object.entries(NIVEIS).map(([chave, v]) => [chave, v.rotulo]),
) as Record<NivelCerteza, string>;

/** O nível de certeza sempre aparece com texto e ícone, nunca só com cor. */
export function SeloCerteza({ nivel }: { nivel: NivelCerteza }) {
  const { rotulo, Icone } = NIVEIS[nivel];
  return (
    <span className={`selo selo-${nivel}`}>
      <Icone tamanho={14} />
      {rotulo}
    </span>
  );
}

export const ROTULO_STATUS: Record<StatusContato, string> = {
  novo: "Novo",
  contatado: "Contatado",
  respondeu: "Respondeu",
  descartado: "Descartado",
};

export function EtiquetaStatus({ status }: { status: StatusContato }) {
  return <span className={`status status-${status}`}>{ROTULO_STATUS[status]}</span>;
}

export function BarraPontuacao({ valor }: { valor: number }) {
  return (
    <div className="pontuacao" role="img" aria-label={`Pontuação ${valor} de 100`}>
      <div className="pontuacao-valor">
        {valor}
        <span> /100</span>
      </div>
      <div className="barra">
        <div style={{ width: `${valor}%` }} />
      </div>
    </div>
  );
}

export function Problemas({ problemas, maximo = 2 }: { problemas: string[]; maximo?: number }) {
  if (problemas.length === 0) return <span className="suave">Nenhum problema detectado</span>;
  const visiveis = problemas.slice(0, maximo);
  const resto = problemas.length - visiveis.length;
  return (
    <>
      {visiveis.map((p) => (
        <span className="tag" key={p}>
          {p}
        </span>
      ))}
      {resto > 0 && (
        <span className="tag tag-mais" title={problemas.slice(maximo).join(", ")}>
          +{resto}
        </span>
      )}
    </>
  );
}
