import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, ApiError } from "../api";
import type { Busca, NovaBusca as ParametrosBusca } from "../api";
import { Alerta } from "../components/Alerta";
import { IconeBusca, IconeCartao, IconeCheck, IconeEscudo, IconeSeta, IconeRelogio } from "../components/Icones";
import { UFS } from "../constantes";

type Fase = "formulario" | "buscando" | "resultado" | "erro";

const SUGESTOES = ["clínicas de estética", "odontologia", "academias", "restaurantes"];
const INTERVALO_MS = 900;

export function NovaBusca() {
  const navegar = useNavigate();
  const [fase, setFase] = useState<Fase>("formulario");
  const [params, setParams] = useState<ParametrosBusca>({
    nicho: "clínicas de estética",
    cidade: "Sorocaba",
    estado: "SP",
    limite: 10,
  });
  const [busca, setBusca] = useState<Busca | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);
  const [erroGeral, setErroGeral] = useState<{ codigo?: string; mensagem: string } | null>(null);
  const montado = useRef(true);

  useEffect(() => {
    montado.current = true;
    return () => {
      montado.current = false;
    };
  }, []);

  // Acompanha o processamento da busca até ela terminar.
  useEffect(() => {
    if (fase !== "buscando" || !busca) return;
    const id = setInterval(async () => {
      try {
        const atual = await api.consultarBusca(busca.id);
        if (!montado.current) return;
        setBusca(atual);
        if (atual.status === "concluida") setFase("resultado");
        else if (atual.status === "erro") {
          setErroGeral({ codigo: atual.erro?.codigo, mensagem: atual.erro?.mensagem ?? "" });
          setFase("erro");
        } else if (atual.status === "cancelada") setFase("formulario");
      } catch (e) {
        if (!montado.current) return;
        setErroGeral({ mensagem: e instanceof Error ? e.message : "Falha ao acompanhar a busca." });
        setFase("erro");
      }
    }, INTERVALO_MS);
    return () => clearInterval(id);
  }, [fase, busca?.id]);

  async function iniciar(dados: ParametrosBusca) {
    setAviso(null);
    setErroGeral(null);
    try {
      const criada = await api.criarBusca(dados);
      setBusca(criada);
      setFase("buscando");
    } catch (e) {
      setErroGeral({
        codigo: e instanceof ApiError ? String(e.status) : undefined,
        mensagem: e instanceof Error ? e.message : "Não foi possível iniciar a busca.",
      });
      setFase("erro");
    }
  }

  function enviar(evento: FormEvent) {
    evento.preventDefault();
    void iniciar({ ...params, nicho: params.nicho.trim(), cidade: params.cidade.trim() });
  }

  async function cancelar() {
    if (!busca) return;
    try {
      await api.cancelarBusca(busca.id);
    } catch {
      /* se falhar, o acompanhamento mostra o estado real */
    }
    setAviso("Busca cancelada.");
    setFase("formulario");
  }

  const pronto = params.nicho.trim().length >= 2 && params.cidade.trim().length >= 2;

  if (fase === "buscando") {
    return (
      <>
        <div className="titulo">
          <h1>Buscando empresas</h1>
          <p className="suave">
            {params.nicho} em {params.cidade}, {params.estado}
          </p>
        </div>
        <section className="cartao cartao-corpo" aria-live="polite" aria-busy="true">
          <ol className="etapas">
            {(busca?.etapas ?? []).map((etapa, i) => (
              <li key={etapa.chave} className={etapa.estado}>
                <span className="marcador">{etapa.estado === "concluida" ? <IconeCheck tamanho={14} /> : i + 1}</span>
                <span>
                  {etapa.rotulo}
                  <span className="sr-only"> ({etapa.estado})</span>
                </span>
              </li>
            ))}
          </ol>
          <div style={{ marginTop: 24 }}>
            <button className="btn" onClick={cancelar}>
              Cancelar busca
            </button>
          </div>
        </section>
      </>
    );
  }

  if (fase === "resultado" && busca) {
    return (
      <>
        <div className="cabecalho-pagina">
          <div className="titulo">
            <h1>Resultado da busca</h1>
            <p className="suave">
              Lote processado para “{busca.nicho}” em {busca.cidade}, {busca.estado}.
            </p>
          </div>
          <div className="acoes">
            <button className="btn" onClick={() => setFase("formulario")}>
              Fazer nova busca
            </button>
            <Link to="/oportunidades" className="btn btn-primario">
              Ver oportunidades <IconeSeta />
            </Link>
          </div>
        </div>

        <section className="cartao resumo-lote">
          <div className="icone-grande">
            <IconeCheck />
          </div>
          <div>
            <h2>Lote de prospecção pronto</h2>
            <p>
              <strong>
                {busca.total_encontradas} {busca.total_encontradas === 1 ? "empresa encontrada" : "empresas encontradas"}
              </strong>
              {busca.duplicadas > 0 &&
                `, ${busca.duplicadas} já ${busca.duplicadas === 1 ? "estava" : "estavam"} na sua carteira e não ${busca.duplicadas === 1 ? "foi duplicada" : "foram duplicadas"}`}
              .
            </p>
          </div>
          <span className="contador" style={{ marginLeft: "auto" }}>
            {busca.novas} {busca.novas === 1 ? "nova adicionada" : "novas adicionadas"}
          </span>
        </section>

        {busca.previa.length === 0 ? (
          <Alerta tipo="info" titulo="Nada de novo neste lote">
            Todas as empresas encontradas já estavam na sua carteira.
          </Alerta>
        ) : (
          <section className="cartao">
            <div className="cartao-cabeca">
              <h2>Prévia das empresas adicionadas</h2>
              <span className="contador">{busca.previa.length} itens</span>
            </div>
            <div className="tabela-wrap">
              <table className="tabela">
                <thead>
                  <tr>
                    <th>Empresa</th>
                    <th>Localização</th>
                    <th>Gargalo detectado</th>
                    <th>Pontuação</th>
                    <th>Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {busca.previa.map((p) => (
                    <tr key={p.oportunidade_id}>
                      <td className="sem-rotulo">
                        <div className="nome">{p.empresa}</div>
                        <div className="nicho">{p.bairro}</div>
                      </td>
                      <td data-rotulo="Localização">
                        {p.cidade} - {p.estado}
                      </td>
                      <td data-rotulo="Gargalo">
                        {p.gargalo ? <span className="tag">{p.gargalo}</span> : <span className="suave">Nenhum</span>}
                      </td>
                      <td data-rotulo="Pontuação">
                        <strong>{p.pontuacao}</strong>/100
                      </td>
                      <td className="sem-rotulo">
                        <button
                          className="btn-link"
                          onClick={() => navegar(`/oportunidades?abrir=${p.oportunidade_id}`)}
                          aria-label={`Explorar ${p.empresa}`}
                        >
                          Explorar →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </>
    );
  }

  if (fase === "erro") {
    return (
      <>
        <div className="titulo">
          <h1>Nova busca de empresas</h1>
        </div>
        <Alerta tipo="erro" titulo="Não foi possível concluir a busca">
          <p>{erroGeral?.mensagem}</p>
          {erroGeral?.codigo && <p className="suave">Código do erro: {erroGeral.codigo}</p>}
        </Alerta>
        <div className="acoes">
          <button className="btn btn-primario" onClick={() => void iniciar(params)}>
            Tentar novamente
          </button>
          <button className="btn" onClick={() => setFase("formulario")}>
            Voltar ao formulário
          </button>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="titulo">
        <h1>Nova busca de empresas</h1>
        <p className="suave">
          Defina o nicho e a localização para encontrar empresas com potencial de melhoria digital.
        </p>
      </div>
      {aviso && <Alerta tipo="info" aoFechar={() => setAviso(null)}>{aviso}</Alerta>}
      <form className="cartao cartao-corpo" onSubmit={enviar} style={{ display: "flex", flexDirection: "column", gap: 18 }}>
        <div className="campo">
          <label htmlFor="nicho">Nicho de atuação</label>
          <input
            id="nicho"
            value={params.nicho}
            onChange={(e) => setParams({ ...params, nicho: e.target.value })}
            placeholder="Ex.: clínicas, academias, restaurantes"
            required
          />
          <div className="sugestoes">
            Sugestões rápidas:
            {SUGESTOES.map((s) => (
              <button type="button" key={s} className="chip" onClick={() => setParams({ ...params, nicho: s })}>
                {s}
              </button>
            ))}
          </div>
        </div>
        <div className="grade-3">
          <div className="campo">
            <label htmlFor="cidade">Cidade</label>
            <input id="cidade" value={params.cidade} onChange={(e) => setParams({ ...params, cidade: e.target.value })} required />
          </div>
          <div className="campo">
            <label htmlFor="estado">Estado</label>
            <select id="estado" value={params.estado} onChange={(e) => setParams({ ...params, estado: e.target.value })}>
              {UFS.map((uf) => (
                <option key={uf}>{uf}</option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="limite">Resultados máximos</label>
            <select id="limite" value={params.limite} onChange={(e) => setParams({ ...params, limite: Number(e.target.value) })}>
              {[5, 10, 15, 20, 30].map((n) => (
                <option key={n} value={n}>
                  {n} empresas
                </option>
              ))}
            </select>
          </div>
        </div>
        <Alerta tipo="info">
          O LeadForge analisa o site de cada empresa (HTTPS, versão para celular, WhatsApp, formulário e
          chamada para ação) e informa o nível de certeza de cada achado.
        </Alerta>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button className="btn btn-primario" disabled={!pronto}>
            <IconeBusca /> Buscar empresas
          </button>
        </div>
      </form>
      <div className="faixa-info">
        <div className="cartao">
          <IconeEscudo />
          <div>
            <strong>Validação da carteira</strong>
            <span>Evita duplicações automaticamente</span>
          </div>
        </div>
        <div className="cartao">
          <IconeRelogio />
          <div>
            <strong>Análise do site</strong>
            <span>HTTPS, responsividade e contato</span>
          </div>
        </div>
        <div className="cartao">
          <IconeCartao />
          <div>
            <strong>Dados públicos</strong>
            <span>Telefone, endereço e site da empresa</span>
          </div>
        </div>
      </div>
    </>
  );
}
