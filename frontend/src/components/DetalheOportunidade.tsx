import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { OportunidadeDetalhe } from "../api";
import { ROTULO_EVIDENCIA } from "../constantes";
import { Alerta } from "./Alerta";
import { IconeFechar } from "./Icones";
import { BarraPontuacao, EtiquetaStatus, SeloCerteza } from "./Selos";

export function DetalheOportunidade({ id, aoFechar }: { id: number; aoFechar: () => void }) {
  const [dados, setDados] = useState<OportunidadeDetalhe | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const botaoFechar = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    let ativo = true;
    api
      .oportunidade(id)
      .then((d) => ativo && setDados(d))
      .catch((e: Error) => ativo && setErro(e.message));
    return () => {
      ativo = false;
    };
  }, [id]);

  useEffect(() => {
    botaoFechar.current?.focus();
    const aoTeclar = (e: KeyboardEvent) => e.key === "Escape" && aoFechar();
    document.addEventListener("keydown", aoTeclar);
    return () => document.removeEventListener("keydown", aoTeclar);
  }, [aoFechar]);

  const temDesconhecido = dados?.evidencias.some((e) => e.nivel_certeza === "desconhecido");

  return (
    <div className="fundo-modal" onClick={aoFechar}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="titulo-detalhe"
        onClick={(e) => e.stopPropagation()}
      >
        <header>
          <div>
            <h2 id="titulo-detalhe">{dados?.empresa ?? "Detalhes da oportunidade"}</h2>
            {dados && (
              <p className="suave">
                {dados.nicho} · {dados.cidade}, {dados.estado}
              </p>
            )}
          </div>
          <button ref={botaoFechar} className="btn" onClick={aoFechar} aria-label="Fechar detalhes">
            <IconeFechar />
          </button>
        </header>
        <div className="corpo">
          {erro && <Alerta tipo="erro">{erro}</Alerta>}
          {!dados && !erro && <p>Carregando…</p>}
          {dados && (
            <>
              <dl className="dados-empresa">
                <div>
                  <dt>Posição no ranking</dt>
                  <dd>{dados.posicao}º</dd>
                </div>
                <div>
                  <dt>Pontuação</dt>
                  <dd>
                    <BarraPontuacao valor={dados.pontuacao} />
                  </dd>
                </div>
                <div>
                  <dt>Endereço</dt>
                  <dd>{[dados.endereco, dados.bairro].filter(Boolean).join(" · ") || "Não informado"}</dd>
                </div>
                <div>
                  <dt>Telefone</dt>
                  <dd>{dados.telefone ?? "Não informado"}</dd>
                </div>
                <div>
                  <dt>Site</dt>
                  <dd>
                    {dados.url_site ? (
                      <a href={dados.url_site} target="_blank" rel="noopener noreferrer">
                        {dados.url_site}
                      </a>
                    ) : (
                      "Não encontrado"
                    )}
                  </dd>
                </div>
                <div>
                  <dt>Status do contato</dt>
                  <dd>
                    <EtiquetaStatus status={dados.status_contato} />
                  </dd>
                </div>
              </dl>

              <h3>Evidências coletadas</h3>
              <div className="tabela-wrap cartao">
                <table className="tabela">
                  <thead>
                    <tr>
                      <th>Evidência</th>
                      <th>Resultado</th>
                      <th>Certeza</th>
                      <th>Fonte</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dados.evidencias.map((e) => (
                      <tr key={e.tipo + e.valor}>
                        <td data-rotulo="Evidência">{ROTULO_EVIDENCIA[e.tipo] ?? e.tipo}</td>
                        <td data-rotulo="Resultado">{e.valor}</td>
                        <td data-rotulo="Certeza">
                          <SeloCerteza nivel={e.nivel_certeza} />
                        </td>
                        <td data-rotulo="Fonte" className="suave">
                          {e.origem_fonte}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {temDesconhecido && (
                <Alerta tipo="info">
                  Ausência de informação não é confirmação de problema: itens marcados como
                  “Desconhecido” precisam ser verificados manualmente.
                </Alerta>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
