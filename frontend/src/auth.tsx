import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { api, ApiError, sessao } from "./api";
import type { Usuario } from "./api";

interface ContextoAuth {
  usuario: Usuario | null;
  carregando: boolean;
  entrar: (email: string, senha: string, lembrar: boolean) => Promise<void>;
  cadastrar: (d: { nome: string; email: string; senha: string }) => Promise<void>;
  sair: () => void;
}

const Contexto = createContext<ContextoAuth | null>(null);

export function ProvedorAuth({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(() => sessao.ler() !== null);

  useEffect(() => {
    if (!sessao.ler()) return;
    api
      .eu()
      .then(setUsuario)
      .catch((erro) => {
        if (erro instanceof ApiError && erro.status === 401) sessao.limpar();
      })
      .finally(() => setCarregando(false));
  }, []);

  const entrar = useCallback(async (email: string, senha: string, lembrar: boolean) => {
    const resposta = await api.entrar({ email, senha });
    sessao.salvar(resposta.token, lembrar);
    setUsuario(resposta.usuario);
  }, []);

  const cadastrar = useCallback(async (d: { nome: string; email: string; senha: string }) => {
    const resposta = await api.cadastrar({ ...d, aceite_lgpd: true });
    sessao.salvar(resposta.token, true);
    setUsuario(resposta.usuario);
  }, []);

  const sair = useCallback(() => {
    sessao.limpar();
    setUsuario(null);
  }, []);

  const valor = useMemo(
    () => ({ usuario, carregando, entrar, cadastrar, sair }),
    [usuario, carregando, entrar, cadastrar, sair],
  );
  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useAuth(): ContextoAuth {
  const valor = useContext(Contexto);
  if (!valor) throw new Error("useAuth deve ser usado dentro de ProvedorAuth");
  return valor;
}
