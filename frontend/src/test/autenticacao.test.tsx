import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { renderizar, simularApi, USUARIO } from "./ajuda";

describe("rotas protegidas", () => {
  it("leva ao login quem não está autenticado", async () => {
    simularApi({});
    renderizar("/oportunidades");
    expect(await screen.findByRole("heading", { name: "Acesse sua conta" })).toBeInTheDocument();
  });
});

describe("tela Entrar", () => {
  it("mantém o botão desabilitado até preencher e mostra erro de credenciais", async () => {
    const usuario = userEvent.setup();
    simularApi({
      "POST /auth/login": () => ({ status: 401, corpo: { detail: "E-mail ou senha incorretos." } }),
    });
    renderizar("/entrar");
    const botao = screen.getByRole("button", { name: /^Entrar/ });
    expect(botao).toBeDisabled();

    await usuario.type(screen.getByLabelText("E-mail"), "lucas@exemplo.com");
    await usuario.type(screen.getByLabelText("Senha"), "errada123");
    await usuario.click(botao);

    expect(await screen.findByRole("alert")).toHaveTextContent("E-mail ou senha incorretos.");
  });

  it("entra com credenciais corretas e vai para as oportunidades", async () => {
    const usuario = userEvent.setup();
    simularApi({
      "POST /auth/login": () => ({ corpo: { token: "t", usuario: USUARIO } }),
      "GET /oportunidades": () => ({ corpo: { total: 0, itens: [] } }),
    });
    renderizar("/entrar");
    await usuario.type(screen.getByLabelText("E-mail"), "lucas@exemplo.com");
    await usuario.type(screen.getByLabelText("Senha"), "senha-forte-1");
    await usuario.click(screen.getByRole("button", { name: /^Entrar/ }));

    expect(await screen.findByRole("heading", { name: "Oportunidades" })).toBeInTheDocument();
    expect(localStorage.getItem("leadforge.token")).toBe("t");
  });

  it("não guarda o acesso quando 'lembrar' está desmarcado", async () => {
    const usuario = userEvent.setup();
    simularApi({
      "POST /auth/login": () => ({ corpo: { token: "efemero", usuario: USUARIO } }),
      "GET /oportunidades": () => ({ corpo: { total: 0, itens: [] } }),
    });
    renderizar("/entrar");
    await usuario.type(screen.getByLabelText("E-mail"), "lucas@exemplo.com");
    await usuario.type(screen.getByLabelText("Senha"), "senha-forte-1");
    await usuario.click(screen.getByLabelText(/Lembrar meu acesso/));
    await usuario.click(screen.getByRole("button", { name: /^Entrar/ }));

    await screen.findByRole("heading", { name: "Oportunidades" });
    expect(localStorage.getItem("leadforge.token")).toBeNull();
    expect(sessionStorage.getItem("leadforge.token")).toBe("efemero");
  });
});

describe("tela Criar conta", () => {
  async function preencher(usuario: ReturnType<typeof userEvent.setup>, confirmar: string) {
    await usuario.type(screen.getByLabelText("Nome completo"), "Lucas Almeida");
    await usuario.type(screen.getByLabelText("E-mail"), "lucas@exemplo.com");
    await usuario.type(screen.getByLabelText("Senha"), "senha-forte-1");
    await usuario.type(screen.getByLabelText("Confirmar senha"), confirmar);
  }

  it("exige o aceite da LGPD para habilitar o cadastro", async () => {
    const usuario = userEvent.setup();
    simularApi({});
    renderizar("/criar-conta");
    await preencher(usuario, "senha-forte-1");
    const botao = screen.getByRole("button", { name: "Criar conta" });
    expect(botao).toBeDisabled();
    await usuario.click(screen.getByRole("checkbox"));
    expect(botao).toBeEnabled();
  });

  it("não chama a API quando as senhas não conferem", async () => {
    const usuario = userEvent.setup();
    const { chamadas } = simularApi({});
    renderizar("/criar-conta");
    await preencher(usuario, "outra-senha-9");
    await usuario.click(screen.getByRole("checkbox"));
    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(await screen.findByText("As senhas não conferem.")).toBeInTheDocument();
    expect(chamadas).toHaveLength(0);
  });

  it("cadastra e leva ao perfil, com o aceite enviado ao servidor", async () => {
    const usuario = userEvent.setup();
    const { chamadas } = simularApi({
      "POST /auth/cadastro": () => ({ status: 201, corpo: { token: "novo", usuario: USUARIO } }),
      "GET /perfil": () => ({
        corpo: { nome: "Lucas Almeida", email: "lucas@exemplo.com", habilidades: [], servicos: [], cidade: "", estado: "", tom_comunicacao: "Amigável" },
      }),
    });
    renderizar("/criar-conta");
    await preencher(usuario, "senha-forte-1");
    await usuario.click(screen.getByRole("checkbox"));
    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(await screen.findByRole("heading", { name: "Perfil" })).toBeInTheDocument();
    expect(chamadas[0].corpo).toMatchObject({ email: "lucas@exemplo.com", aceite_lgpd: true });
  });

  it("mostra o erro de e-mail já cadastrado", async () => {
    const usuario = userEvent.setup();
    simularApi({ "POST /auth/cadastro": () => ({ status: 409, corpo: { detail: "Já existe uma conta com este e-mail." } }) });
    renderizar("/criar-conta");
    await preencher(usuario, "senha-forte-1");
    await usuario.click(screen.getByRole("checkbox"));
    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));
    await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("Já existe uma conta"));
  });
});
