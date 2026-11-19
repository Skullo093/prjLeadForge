import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { entrarComoUsuario, renderizar, simularApi, USUARIO } from "./ajuda";

const ETAPAS = (estados: string[]) =>
  ["Buscando empresas", "Removendo duplicatas", "Analisando sites"].map((rotulo, i) => ({
    chave: `e${i}`, rotulo, estado: estados[i],
  }));

const BUSCA_BASE = {
  id: 7, nicho: "clínicas de estética", cidade: "Sorocaba", estado: "SP", limite: 10,
  total_encontradas: 0, novas: 0, duplicadas: 0, erro: null, previa: [],
};
const base = { "GET /auth/eu": () => ({ corpo: USUARIO }) };

describe("tela Nova busca", () => {
  it("percorre formulário → buscando → resultado, com duplicadas informadas", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    const { chamadas } = simularApi({
      ...base,
      "POST /buscas": () => ({
        status: 202,
        corpo: { ...BUSCA_BASE, status: "processando", etapas: ETAPAS(["ativa", "pendente", "pendente"]) },
      }),
      "GET /buscas/7": () => ({
        corpo: {
          ...BUSCA_BASE, status: "concluida", etapas: ETAPAS(["concluida", "concluida", "concluida"]),
          total_encontradas: 10, novas: 8, duplicadas: 2,
          previa: [
            { oportunidade_id: 1, empresa: "Clínica Bela Forma", bairro: "Campolim", cidade: "Sorocaba", estado: "SP", gargalo: "Sem versão para celular", pontuacao: 91 },
          ],
        },
      }),
    });
    renderizar("/nova-busca");

    await usuario.click(await screen.findByRole("button", { name: /Buscar empresas/ }));
    expect(await screen.findByRole("heading", { name: "Buscando empresas" })).toBeInTheDocument();
    expect(screen.getByText("Buscando empresas", { selector: "span" })).toBeInTheDocument();

    expect(await screen.findByRole("heading", { name: "Resultado da busca" }, { timeout: 4000 })).toBeInTheDocument();
    expect(screen.getByText(/10 empresas encontradas/)).toBeInTheDocument();
    expect(screen.getByText(/2 já estavam na sua carteira e não foram duplicadas/)).toBeInTheDocument();
    expect(screen.getByText("8 novas adicionadas")).toBeInTheDocument();
    expect(screen.getByText("Clínica Bela Forma")).toBeInTheDocument();
    expect(chamadas.find((c) => c.chave === "POST /buscas")?.corpo).toEqual({ nicho: "clínicas de estética", cidade: "Sorocaba", estado: "SP", limite: 10 });
  });

  it("mostra o estado de erro com código e permite tentar novamente", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    let tentativas = 0;
    simularApi({
      ...base,
      "POST /buscas": () => {
        tentativas += 1;
        return { status: 202, corpo: { ...BUSCA_BASE, status: "processando", etapas: ETAPAS(["ativa", "pendente", "pendente"]) } };
      },
      "GET /buscas/7": () => ({
        corpo: {
          ...BUSCA_BASE, status: "erro", etapas: ETAPAS(["ativa", "pendente", "pendente"]),
          erro: { codigo: "PLACES_503", mensagem: "O serviço de busca está indisponível no momento." },
        },
      }),
    });
    renderizar("/nova-busca");
    await usuario.click(await screen.findByRole("button", { name: /Buscar empresas/ }));

    const alerta = await screen.findByRole("alert", {}, { timeout: 4000 });
    expect(alerta).toHaveTextContent("O serviço de busca está indisponível no momento.");
    expect(alerta).toHaveTextContent("Código do erro: PLACES_503");

    await usuario.click(screen.getByRole("button", { name: "Tentar novamente" }));
    await screen.findByRole("alert", {}, { timeout: 4000 });
    expect(tentativas).toBe(2);
  });

  it("permite cancelar a busca em andamento", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    const { chamadas } = simularApi({
      ...base,
      "POST /buscas": () => ({ status: 202, corpo: { ...BUSCA_BASE, status: "processando", etapas: ETAPAS(["ativa", "pendente", "pendente"]) } }),
      "GET /buscas/7": () => ({ corpo: { ...BUSCA_BASE, status: "processando", etapas: ETAPAS(["concluida", "ativa", "pendente"]) } }),
      "POST /buscas/7/cancelar": () => ({ corpo: { ...BUSCA_BASE, status: "cancelada", etapas: ETAPAS(["ativa", "pendente", "pendente"]) } }),
    });
    renderizar("/nova-busca");
    await usuario.click(await screen.findByRole("button", { name: /Buscar empresas/ }));
    await usuario.click(await screen.findByRole("button", { name: "Cancelar busca" }));

    expect(await screen.findByText("Busca cancelada.")).toBeInTheDocument();
    expect(chamadas.some((c) => c.chave === "POST /buscas/7/cancelar")).toBe(true);
  });

  it("não deixa buscar com campos vazios e oferece sugestões de nicho", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    simularApi(base);
    renderizar("/nova-busca");
    const nicho = await screen.findByLabelText("Nicho de atuação");
    await usuario.clear(nicho);
    expect(screen.getByRole("button", { name: /Buscar empresas/ })).toBeDisabled();
    await usuario.click(screen.getByRole("button", { name: "academias" }));
    expect(nicho).toHaveValue("academias");
    expect(screen.getByRole("button", { name: /Buscar empresas/ })).toBeEnabled();
  });
});
