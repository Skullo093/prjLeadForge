import { useEffect, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import { api } from "../api";
import type { Perfil as PerfilDados } from "../api";
import { Alerta } from "../components/Alerta";
import { IconeFechar, IconeMais } from "../components/Icones";
import { SERVICOS, TONS, UFS } from "../constantes";

export function Perfil() {
  const [original, setOriginal] = useState<PerfilDados | null>(null);
  const [perfil, setPerfil] = useState<PerfilDados | null>(null);
  const [novaHabilidade, setNovaHabilidade] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [sucesso, setSucesso] = useState(false);
  const [salvando, setSalvando] = useState(false);

  useEffect(() => {
    let ativo = true;
    api
      .perfil()
      .then((p) => {
        if (!ativo) return;
        setOriginal(p);
        setPerfil(p);
      })
      .catch((e: Error) => ativo && setErro(e.message));
    return () => {
      ativo = false;
    };
  }, []);

  if (!perfil) {
    return erro ? <Alerta tipo="erro">{erro}</Alerta> : <p>Carregando…</p>;
  }

  const atualizar = (parte: Partial<PerfilDados>) => {
    setSucesso(false);
    setPerfil({ ...perfil, ...parte });
  };

  function adicionarHabilidade() {
    const valor = novaHabilidade.trim();
    if (!valor || !perfil) return;
    if (!perfil.habilidades.some((h) => h.toLowerCase() === valor.toLowerCase())) {
      atualizar({ habilidades: [...perfil.habilidades, valor] });
    }
    setNovaHabilidade("");
  }

  function aoTeclar(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault();
      adicionarHabilidade();
    }
  }

  function alternarServico(servico: string) {
    const atuais = perfil!.servicos;
    atualizar({
      servicos: atuais.includes(servico) ? atuais.filter((s) => s !== servico) : [...atuais, servico],
    });
  }

  async function salvar(evento: FormEvent) {
    evento.preventDefault();
    if (!perfil) return;
    setErro(null);
    setSalvando(true);
    try {
      const salvo = await api.salvarPerfil(perfil);
      setOriginal(salvo);
      setPerfil(salvo);
      setSucesso(true);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não foi possível salvar o perfil.");
    } finally {
      setSalvando(false);
    }
  }

  const servicosVisiveis = [...SERVICOS, ...perfil.servicos.filter((s) => !SERVICOS.includes(s))];

  return (
    <form onSubmit={salvar} style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {sucesso && (
        <Alerta tipo="ok" titulo="Perfil atualizado com sucesso." aoFechar={() => setSucesso(false)}>
          Suas preferências foram salvas.
        </Alerta>
      )}
      {erro && <Alerta tipo="erro">{erro}</Alerta>}

      <div className="titulo">
        <h1>Perfil</h1>
        <p className="suave">
          Informe suas especialidades, localização e tom de comunicação. Eles orientam as sugestões de
          abordagem das próximas etapas.
        </p>
      </div>

      <section className="cartao secao-perfil">
        <header>
          <h2>Dados pessoais</h2>
          <span className="suave">Identificação na plataforma</span>
        </header>
        <div className="grade-2">
          <div className="campo">
            <label htmlFor="nome">Nome completo</label>
            <input id="nome" value={perfil.nome} onChange={(e) => atualizar({ nome: e.target.value })} required minLength={2} />
          </div>
          <div className="campo">
            <label htmlFor="email">E-mail de contato</label>
            <input id="email" type="email" value={perfil.email} onChange={(e) => atualizar({ email: e.target.value })} required />
          </div>
        </div>
      </section>

      <section className="cartao secao-perfil">
        <header>
          <h2>Habilidades</h2>
          <span className="suave">Tecnologias e competências que você domina</span>
        </header>
        <div className="etiquetas" aria-live="polite">
          {perfil.habilidades.length === 0 && <span className="suave">Nenhuma habilidade adicionada.</span>}
          {perfil.habilidades.map((h) => (
            <span className="etiqueta" key={h}>
              {h}
              <button
                type="button"
                aria-label={`Remover ${h}`}
                onClick={() => atualizar({ habilidades: perfil.habilidades.filter((x) => x !== h) })}
              >
                <IconeFechar tamanho={14} />
              </button>
            </span>
          ))}
        </div>
        <div className="linha-adicionar">
          <input
            aria-label="Nova habilidade"
            placeholder="Digite uma competência (ex.: Node.js, SEO)"
            value={novaHabilidade}
            onChange={(e) => setNovaHabilidade(e.target.value)}
            onKeyDown={aoTeclar}
            maxLength={60}
          />
          <button type="button" className="btn" onClick={adicionarHabilidade} disabled={!novaHabilidade.trim()}>
            <IconeMais /> Adicionar
          </button>
        </div>
      </section>

      <section className="cartao secao-perfil">
        <header>
          <h2>Serviços oferecidos</h2>
          <span className="suave">Selecione o que você vende</span>
        </header>
        <div className="opcoes">
          {servicosVisiveis.map((s) => (
            <label className="opcao" key={s}>
              <input type="checkbox" checked={perfil.servicos.includes(s)} onChange={() => alternarServico(s)} />
              {s}
            </label>
          ))}
        </div>
      </section>

      <section className="cartao secao-perfil">
        <header>
          <h2>Localização</h2>
          <span className="suave">Onde você atua</span>
        </header>
        <div className="grade-2">
          <div className="campo">
            <label htmlFor="cidade">Cidade</label>
            <input id="cidade" value={perfil.cidade} onChange={(e) => atualizar({ cidade: e.target.value })} />
          </div>
          <div className="campo">
            <label htmlFor="estado">Estado</label>
            <select id="estado" value={perfil.estado} onChange={(e) => atualizar({ estado: e.target.value })}>
              <option value="">Selecione</option>
              {UFS.map((uf) => (
                <option key={uf}>{uf}</option>
              ))}
            </select>
          </div>
        </div>
      </section>

      <section className="cartao secao-perfil">
        <header>
          <h2>Tom de comunicação</h2>
          <span className="suave">Como você prefere falar com clientes</span>
        </header>
        <div className="opcoes tres" role="radiogroup" aria-label="Tom de comunicação">
          {TONS.map((tom) => (
            <label className="opcao" key={tom}>
              <input type="radio" name="tom" checked={perfil.tom_comunicacao === tom} onChange={() => atualizar({ tom_comunicacao: tom })} />
              {tom}
            </label>
          ))}
        </div>
      </section>

      <div className="barra-salvar">
        <span className="suave">Alterações não salvas serão perdidas ao sair desta página.</span>
        <div className="acoes">
          <button type="button" className="btn" onClick={() => { setPerfil(original); setSucesso(false); }}>
            Cancelar
          </button>
          <button className="btn btn-primario" disabled={salvando}>
            {salvando ? "Salvando…" : "Salvar alterações"}
          </button>
        </div>
      </div>
    </form>
  );
}
