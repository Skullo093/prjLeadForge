import { useState } from "react";
import type { FormEvent } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { ApiError } from "../api";
import { useAuth } from "../auth";
import { Alerta } from "../components/Alerta";
import { IconeOlho, IconeOlhoRiscado, IconeSeta } from "../components/Icones";
import { PaginaEntrada } from "../components/PaginaEntrada";

export function Entrar() {
  const { usuario, entrar } = useAuth();
  const local = useLocation();
  const destino = (local.state as { de?: string } | null)?.de ?? "/oportunidades";
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [lembrar, setLembrar] = useState(true);
  const [mostrar, setMostrar] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to={destino} replace />;

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      await entrar(email.trim(), senha, lembrar);
    } catch (e) {
      setErro(e instanceof ApiError ? e.message : "Não foi possível entrar. Tente novamente.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <PaginaEntrada>
      <form className="cartao formulario-entrada" onSubmit={enviar} noValidate>
        <div>
          <h2>Acesse sua conta</h2>
          <p className="suave">Insira suas credenciais para continuar.</p>
        </div>
        {erro && <Alerta tipo="erro">{erro}</Alerta>}
        <div className="campo">
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="campo">
          <label htmlFor="senha">Senha</label>
          <div className="com-icone">
            <input
              id="senha"
              type={mostrar ? "text" : "password"}
              autoComplete="current-password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
            <button
              type="button"
              className="icone-direita"
              onClick={() => setMostrar((v) => !v)}
              aria-label={mostrar ? "Ocultar senha" : "Mostrar senha"}
            >
              {mostrar ? <IconeOlhoRiscado /> : <IconeOlho />}
            </button>
          </div>
        </div>
        <label className="checkbox">
          <input type="checkbox" checked={lembrar} onChange={(e) => setLembrar(e.target.checked)} />
          Lembrar meu acesso neste navegador
        </label>
        <button className="btn btn-primario btn-largo" disabled={enviando || !email || !senha}>
          {enviando ? "Entrando…" : "Entrar"} <IconeSeta />
        </button>
        <p className="centro suave">
          Ainda não tem conta? <Link to="/criar-conta">Criar conta</Link>
        </p>
      </form>
    </PaginaEntrada>
  );
}
