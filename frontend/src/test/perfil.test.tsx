import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { ApiError, api } from "../api";
import { entrarComoUsuario, renderizar, simularApi, USUARIO } from "./ajuda";

const PERFIL = {
  nome: "Lucas Almeida", email: "lucas@exemplo.com", habilidades: ["React"], servicos: [],
  cidade: "", estado: "", tom_comunicacao: "Amigável",
};

describe("tela Perfil", () => {
  it("adiciona habilidades sem repetir, escolhe serviços e salva", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    const { chamadas } = simularApi({
      "GET /auth/eu": () => ({ corpo: USUARIO }),
      "GET /perfil": () => ({ corpo: PERFIL }),
      "PUT /perfil": (corpo) => ({ corpo }),
    });
    renderizar("/perfil");

    const campo = await screen.findByLabelText("Nova habilidade");
    await usuario.type(campo, "Python{Enter}");
    await usuario.type(campo, "react{Enter}"); // repetida (ignora maiúsculas)
    await usuario.click(screen.getByLabelText("Criação de site"));
    await usuario.click(screen.getByLabelText("Direto"));
    await usuario.click(screen.getByRole("button", { name: "Salvar alterações" }));

    expect(await screen.findByText("Perfil atualizado com sucesso.")).toBeInTheDocument();
    expect(chamadas.at(-1)?.corpo).toMatchObject({
      habilidades: ["React", "Python"], servicos: ["Criação de site"], tom_comunicacao: "Direto",
    });
  });

  it("remove habilidade e Cancelar desfaz as alterações", async () => {
    const usuario = userEvent.setup();
    entrarComoUsuario();
    simularApi({ "GET /auth/eu": () => ({ corpo: USUARIO }), "GET /perfil": () => ({ corpo: PERFIL }) });
    renderizar("/perfil");

    await usuario.click(await screen.findByRole("button", { name: "Remover React" }));
    expect(screen.getByText("Nenhuma habilidade adicionada.")).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Cancelar" }));
    expect(screen.getByText("React")).toBeInTheDocument();
  });
});

describe("cliente da API", () => {
  it("transforma falha de rede em mensagem amigável", async () => {
    const { vi } = await import("vitest");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fetch failed")));
    await expect(api.perfil()).rejects.toMatchObject({ status: 0, message: expect.stringContaining("Sem conexão") });
  });

  it("usa a mensagem de validação do servidor", async () => {
    simularApi({
      "PUT /perfil": () => ({ status: 422, corpo: { detail: [{ msg: "Value error, Informe uma UF válida." }] } }),
    });
    const erro = await api.salvarPerfil(PERFIL as never).catch((e: unknown) => e);
    expect(erro).toBeInstanceOf(ApiError);
    expect((erro as ApiError).message).toBe("Informe uma UF válida.");
  });
});
