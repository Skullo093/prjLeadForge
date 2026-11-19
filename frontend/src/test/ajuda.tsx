import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import { App } from "../App";
import { ProvedorAuth } from "../auth";

export type Manipulador = (corpo: unknown, url: URL) => { status?: number; corpo?: unknown } | Promise<{ status?: number; corpo?: unknown }>;

/** Simula o backend: cada chave é "MÉTODO /caminho" (sem o prefixo /api). */
export function simularApi(rotas: Record<string, Manipulador>) {
  const chamadas: { chave: string; corpo: unknown }[] = [];
  const fetchFalso = vi.fn(async (entrada: RequestInfo | URL, opcoes?: RequestInit) => {
    const url = new URL(String(entrada), "http://localhost");
    const metodo = opcoes?.method ?? "GET";
    const chave = `${metodo} ${url.pathname.replace(/^\/api/, "")}`;
    const corpo = opcoes?.body ? JSON.parse(String(opcoes.body)) : undefined;
    chamadas.push({ chave, corpo });
    const manipulador = rotas[chave];
    if (!manipulador) return new Response(JSON.stringify({ detail: `rota não simulada: ${chave}` }), { status: 500 });
    const { status = 200, corpo: resposta } = await manipulador(corpo, url);
    return new Response(JSON.stringify(resposta ?? {}), { status, headers: { "Content-Type": "application/json" } });
  });
  vi.stubGlobal("fetch", fetchFalso);
  return { chamadas, fetchFalso };
}

export function entrarComoUsuario() {
  localStorage.setItem("leadforge.token", "token-teste");
}

export function renderizar(rota: string) {
  return render(
    <MemoryRouter initialEntries={[rota]}>
      <ProvedorAuth>
        <App />
      </ProvedorAuth>
    </MemoryRouter>,
  );
}

export const USUARIO = { id: 1, email: "lucas@exemplo.com" };

export const OPORTUNIDADES = [
  {
    id: 1, posicao: 1, empresa: "Clínica Bela Forma", nicho: "clínicas de estética", cidade: "Sorocaba", estado: "SP",
    pontuacao: 91, problemas: ["Sem versão para celular", "Site não seguro (sem HTTPS)", "Sem botão de WhatsApp"],
    nivel_certeza: "sinal_forte", status_contato: "novo",
  },
  {
    id: 2, posicao: 2, empresa: "Espaço Vita Estética", nicho: "clínicas de estética", cidade: "Sorocaba", estado: "SP",
    pontuacao: 64, problemas: ["Sem site encontrado"], nivel_certeza: "desconhecido", status_contato: "novo",
  },
];
