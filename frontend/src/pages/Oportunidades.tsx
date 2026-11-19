import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api";
import type { NivelCerteza, Oportunidade, StatusContato } from "../api";
import { Alerta } from "../components/Alerta";
import { DetalheOportunidade } from "../components/DetalheOportunidade";
import { IconeBaixar, IconeBusca, IconeFechar } from "../components/Icones";
import {
  BarraPontuacao,
  EtiquetaStatus,
  Problemas,
  ROTULO_NIVEL,
  ROTULO_STATUS,
  SeloCerteza,
} from "../components/Selos";

export function Oportunidades() {
  const [parametros, setParametros] = useSearchParams();
  const [busca, setBusca] = useState("");
  const [status, setStatus] = useState<StatusContato | "">("");
  const [certeza, setCerteza] = useState<NivelCerteza | "">("");
  const [itens, setItens] = useState<Oportunidade[] | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const abertaId = Number(parametros.get("abrir")) || null;

  useEffect(() => {
    let ativo = true;
    const espera = setTimeout(() => {
      api
        .oportunidades({ q: busca.trim(), status_contato: status, nivel_certeza: certeza })
        .then((r) => {
          if (!ativo) return;
          setItens(r.itens);
          setErro(null);
        })
        .catch((e: Error) => ativo && setErro(e.message));
    }, 250);
    return () => {
      ativo = false;
      clearTimeout(espera);
    };
  }, [busca, status, certeza]);

  const filtrando = busca !== "" || status !== "" || certeza !== "";
  const limpar = () => {
    setBusca("");
    setStatus("");
    setCerteza("");
  };
  const abrir = (id: number) => setParametros({ abrir: String(id) });
  const fechar = () => setParametros({});

  return (
    <>
      <div className="cabecalho-pagina">
        <div className="titulo">
          <div className="linha">
            <h1>Oportunidades</h1>
            {itens && (
              <span className="contador">
                {itens.length} {itens.length === 1 ? "oportunidade encontrada" : "oportunidades encontradas"}
              </span>
            )}
          </div>
          <p className="suave">Empresas ordenadas da maior para a menor pontuação.</p>
        </div>
        <div className="acoes">
          <button className="btn" disabled title="A exportação estará disponível nas próximas etapas">
            <IconeBaixar /> Exportar
          </button>
          <Link to="/nova-busca" className="btn btn-primario">
            <IconeBusca /> Nova busca
          </Link>
        </div>
      </div>

      <div className="cartao filtros" role="search">
        <div className="campo busca">
          <label htmlFor="filtro-nome">Buscar por nome</label>
          <input
            id="filtro-nome"
            type="search"
            placeholder="Nome da empresa…"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>
        <div className="campo">
          <label htmlFor="filtro-status">Status do contato</label>
          <select id="filtro-status" value={status} onChange={(e) => setStatus(e.target.value as StatusContato | "")}>
            <option value="">Todos</option>
            {(Object.keys(ROTULO_STATUS) as StatusContato[]).map((s) => (
              <option key={s} value={s}>
                {ROTULO_STATUS[s]}
              </option>
            ))}
          </select>
        </div>
        <div className="campo">
          <label htmlFor="filtro-certeza">Nível de certeza</label>
          <select id="filtro-certeza" value={certeza} onChange={(e) => setCerteza(e.target.value as NivelCerteza | "")}>
            <option value="">Todos</option>
            {(Object.keys(ROTULO_NIVEL) as NivelCerteza[]).map((n) => (
              <option key={n} value={n}>
                {ROTULO_NIVEL[n]}
              </option>
            ))}
          </select>
        </div>
        {filtrando && (
          <button className="btn-link" onClick={limpar}>
            <IconeFechar tamanho={14} /> Limpar filtros
          </button>
        )}
      </div>

      {erro && <Alerta tipo="erro">{erro}</Alerta>}

      {itens && itens.length === 0 && (
        <div className="cartao vazio">
          {filtrando ? (
            <>
              <h2>Nenhuma oportunidade com esses filtros</h2>
              <p className="suave">Tente outro nome ou limpe os filtros.</p>
              <button className="btn" onClick={limpar}>
                Limpar filtros
              </button>
            </>
          ) : (
            <>
              <h2>Nenhuma oportunidade ainda</h2>
              <p className="suave">Faça sua primeira busca para encontrar empresas.</p>
              <Link to="/nova-busca" className="btn btn-primario">
                Nova busca
              </Link>
            </>
          )}
        </div>
      )}

      {itens && itens.length > 0 && (
        <div className="cartao tabela-wrap">
          <table className="tabela">
            <thead>
              <tr>
                <th>#</th>
                <th>Empresa e nicho</th>
                <th>Cidade</th>
                <th>Pontuação</th>
                <th>Problemas detectados</th>
                <th>Nível de certeza</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {itens.map((o) => (
                <tr key={o.id}>
                  <td data-rotulo="Posição">{o.posicao}</td>
                  <td className="sem-rotulo">
                    <div className="nome">{o.empresa}</div>
                    <div className="nicho">{o.nicho}</div>
                  </td>
                  <td data-rotulo="Cidade">
                    {o.cidade}, {o.estado}
                  </td>
                  <td className="sem-rotulo">
                    <BarraPontuacao valor={o.pontuacao} />
                  </td>
                  <td className="sem-rotulo">
                    <Problemas problemas={o.problemas} />
                  </td>
                  <td className="sem-rotulo">
                    <SeloCerteza nivel={o.nivel_certeza} />
                  </td>
                  <td className="sem-rotulo">
                    <EtiquetaStatus status={o.status_contato} />
                  </td>
                  <td className="sem-rotulo">
                    <button className="btn-link" onClick={() => abrir(o.id)} aria-label={`Ver detalhes de ${o.empresa}`}>
                      Ver detalhes →
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {abertaId && <DetalheOportunidade id={abertaId} aoFechar={fechar} />}
    </>
  );
}
