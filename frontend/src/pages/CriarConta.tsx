import { useRef, useState } from "react";
import type { FormEvent } from "react";
import { Link, Navigate } from "react-router-dom";
import { ApiError } from "../api";
import { useAuth } from "../auth";
import { Alerta } from "../components/Alerta";
import { PaginaEntrada } from "../components/PaginaEntrada";

export function CriarConta() {
  const { usuario, cadastrar } = useAuth();
  // Depois de cadastrar, o usuário vai para o perfil (e não para a lista de oportunidades).
  const destino = useRef("/oportunidades");
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmar, setConfirmar] = useState("");
  const [aceite, setAceite] = useState(false);
  const [erroSenha, setErroSenha] = useState<string | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to={destino.current} replace />;

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    setErro(null);
    setErroSenha(null);
    if (senha.length < 8) return setErroSenha("A senha precisa ter pelo menos 8 caracteres.");
    if (senha !== confirmar) return setErroSenha("As senhas não conferem.");
    setEnviando(true);
    destino.current = "/perfil";
    try {
      await cadastrar({ nome: nome.trim(), email: email.trim(), senha });
    } catch (e) {
      destino.current = "/oportunidades";
      setErro(e instanceof ApiError ? e.message : "Não foi possível criar a conta.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <PaginaEntrada>
      <form className="cartao formulario-entrada" onSubmit={enviar} noValidate>
        <div>
          <h2>Criar conta</h2>
          <p className="suave">Cadastre-se para começar a prospectar.</p>
        </div>
        {erro && <Alerta tipo="erro">{erro}</Alerta>}
        <div className="campo">
          <label htmlFor="nome">Nome completo</label>
          <input id="nome" autoComplete="name" value={nome} onChange={(e) => setNome(e.target.value)} required />
        </div>
        <div className="campo">
          <label htmlFor="email">E-mail</label>
          <input id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="campo">
          <label htmlFor="senha">Senha</label>
          <input
            id="senha"
            type="password"
            autoComplete="new-password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            aria-invalid={erroSenha !== null}
            aria-describedby={erroSenha ? "erro-senha" : undefined}
            required
          />
          <small>Mínimo de 8 caracteres.</small>
        </div>
        <div className="campo">
          <label htmlFor="confirmar">Confirmar senha</label>
          <input
            id="confirmar"
            type="password"
            autoComplete="new-password"
            value={confirmar}
            onChange={(e) => setConfirmar(e.target.value)}
            aria-invalid={erroSenha !== null}
            required
          />
          {erroSenha && (
            <span id="erro-senha" className="erro-campo" role="alert">
              {erroSenha}
            </span>
          )}
        </div>
        <label className="checkbox">
          <input type="checkbox" checked={aceite} onChange={(e) => setAceite(e.target.checked)} />
          <span>Concordo com o uso de dados públicos de empresas, conforme a LGPD.</span>
        </label>
        <button className="btn btn-primario btn-largo" disabled={enviando || !aceite || !nome || !email || !senha}>
          {enviando ? "Criando…" : "Criar conta"}
        </button>
        <p className="centro suave">
          Já tem conta? <Link to="/entrar">Entrar</Link>
        </p>
      </form>
    </PaginaEntrada>
  );
}
