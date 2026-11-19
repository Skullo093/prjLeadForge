import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { entrarComoUsuario, OPORTUNIDADES, renderizar, simularApi, USUARIO } from "./ajuda";

const base = { "GET /auth/eu": () => ({ corpo: USUARIO }) };

describe("tela Oportunidades", () => {
  it("lista as empresas com pontuação, certeza e problemas", async () => {
    entrarComoUsuario();
    simularApi({ ...base, "GET /oportunidades": () => ({ corpo: { total: 2, itens: OPORTUNIDADES } }) });
    renderizar("/oportunidades");

    const linhas = await screen.findAllByRole("row");
    expect(linhas).toHaveLength(3); // cabeçalho + 2
    const primeira = within(linhas[1]);
    expect(primeira.getByText("Clínica Bela Forma")).toBeInTheDocument();
    expect(primeira.getByText("Sinal forte")).toBeInTheDocument();
    expect(primeira.getByText("Sem versão para celular")).toBeInTheDocument();
    expect(primeira.getByText("+1")).toBeInTheDocument();
    expect(primeira.getByRole("img", { name: "Pontuação 91 de 100" })).toBeInTheDocument();
    expect(within(linhas[2]).getByText("Desconhecido")).toBeInTheDocument();
  });

  it("mostra o estado vazio e convida a fazer a primeira busca", async () => {
    entrarComoUsuario();
    simularApi({ ...base, "GET /oportunidades": () => ({ corpo: { total: 0, itens: [] } }) });
    renderizar("/oportunidades");
    const titulo = await screen.findByText("Nenhuma oportunidade ainda");
    const cartao = titulo.closest(".vazio") as HTMLElement;
    expect(within(cartao).getByRole("link", { name: "Nova busca" })).toHaveAttribute("href", "/nova-busca");
  });

  it("envia os filtros para a API e mostra o estado de filtro sem resultado", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    const consultas: string[] = [];
    simularApi({
      ...base,
      "GET /oportunidades": (_, url) => {
        consultas.push(url.search);
        return { corpo: url.search ? { total: 0, itens: [] } : { total: 2, itens: OPORTUNIDADES } };
      },
    });
    renderizar("/oportunidades");
    await screen.findByText("Clínica Bela Forma");

    await usuario.selectOptions(screen.getByLabelText("Nível de certeza"), "desconhecido");
    expect(await screen.findByText("Nenhuma oportunidade com esses filtros")).toBeInTheDocument();
    expect(consultas.some((c) => c.includes("nivel_certeza=desconhecido"))).toBe(true);

    await usuario.click(screen.getAllByRole("button", { name: /Limpar filtros/ })[0]);
    expect(await screen.findByText("Clínica Bela Forma")).toBeInTheDocument();
  });

  it("abre o detalhe com as evidências e o aviso sobre itens desconhecidos", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    simularApi({
      ...base,
      "GET /oportunidades": () => ({ corpo: { total: 2, itens: OPORTUNIDADES } }),
      "GET /oportunidades/2": () => ({
        corpo: {
          ...OPORTUNIDADES[1], bairro: "Centro", endereco: "Rua A, 10", telefone: null, url_site: null,
          evidencias: [
            { tipo: "disponibilidade_site", valor: "Site não encontrado", nivel_certeza: "desconhecido",
              origem_fonte: "Dados da empresa (API de lugares)", indica_problema: true, coletada_em: "2026-11-19T10:00:00Z" },
          ],
        },
      }),
    });
    renderizar("/oportunidades");
    await usuario.click(await screen.findByRole("button", { name: "Ver detalhes de Espaço Vita Estética" }));

    const modal = await screen.findByRole("dialog");
    expect(await within(modal).findByText("Site não encontrado")).toBeInTheDocument();
    expect(within(modal).getByText(/Ausência de informação não é confirmação de problema/)).toBeInTheDocument();
    await usuario.keyboard("{Escape}");
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("deixa o botão Exportar desabilitado nesta etapa", async () => {
    entrarComoUsuario();
    simularApi({ ...base, "GET /oportunidades": () => ({ corpo: { total: 0, itens: [] } }) });
    renderizar("/oportunidades");
    expect(await screen.findByRole("button", { name: /Exportar/ })).toBeDisabled();
  });
});
