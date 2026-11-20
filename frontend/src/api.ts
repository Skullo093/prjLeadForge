export type NivelCerteza = "confirmado" | "sinal_forte" | "inferencia" | "desconhecido";
export type StatusContato = "novo" | "contatado" | "respondeu" | "descartado";
export type StatusBusca = "processando" | "concluida" | "erro" | "cancelada";

export interface Usuario {
  id: number;
  email: string;
}
export interface Perfil {
  nome: string;
  email: string;
  habilidades: string[];
  servicos: string[];
  cidade: string;
  estado: string;
  tom_comunicacao: "Formal" | "Amigável" | "Direto";
}
export interface Oportunidade {
  id: number;
  posicao: number;
  empresa: string;
  nicho: string;
  cidade: string;
  estado: string;
  pontuacao: number;
  problemas: string[];
  nivel_certeza: NivelCerteza;
  status_contato: StatusContato;
}
export interface Evidencia {
  tipo: string;
  valor: string;
  nivel_certeza: NivelCerteza;
  origem_fonte: string;
  indica_problema: boolean;
  coletada_em: string;
}
export interface OportunidadeDetalhe extends Oportunidade {
  bairro: string | null;
  endereco: string | null;
  telefone: string | null;
  url_site: string | null;
  evidencias: Evidencia[];
}
export interface Etapa {
  chave: string;
  rotulo: string;
  estado: "concluida" | "ativa" | "pendente";
}
export interface Previa {
  oportunidade_id: number;
  empresa: string;
  bairro: string | null;
  cidade: string;
  estado: string;
  gargalo: string | null;
  pontuacao: number;
}
export interface Busca {
  id: number;
  nicho: string;
  cidade: string;
  estado: string;
  limite: number;
  status: StatusBusca;
  etapas: Etapa[];
  total_encontradas: number;
  novas: number;
  duplicadas: number;
  erro: { codigo: string; mensagem: string } | null;
  previa: Previa[];
}
export interface NovaBusca {
  nicho: string;
  cidade: string;
  estado: string;
  limite: number;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

const BASE = import.meta.env.VITE_API_URL ?? "/api";
const CHAVE_TOKEN = "leadforge.token";

export const sessao = {
  ler(): string | null {
    try {
      return localStorage.getItem(CHAVE_TOKEN) ?? sessionStorage.getItem(CHAVE_TOKEN);
    } catch {
      return null;
    }
  },
  salvar(token: string, lembrar: boolean) {
    this.limpar();
    try {
      (lembrar ? localStorage : sessionStorage).setItem(CHAVE_TOKEN, token);
    } catch {
      /* armazenamento indisponível: a sessão vale só até recarregar a página */
    }
  },
  limpar() {
    try {
      localStorage.removeItem(CHAVE_TOKEN);
      sessionStorage.removeItem(CHAVE_TOKEN);
    } catch {
      /* ignorado */
    }
  },
};

function mensagemDeErro(corpo: unknown, status: number): string {
  const detalhe = (corpo as { detail?: unknown } | null)?.detail;
  if (typeof detalhe === "string") return detalhe;
  if (Array.isArray(detalhe) && detalhe.length > 0) {
    const primeiro = detalhe[0] as { msg?: string };
    return (primeiro.msg ?? "Dados inválidos.").replace(/^Value error, /, "");
  }
  return status >= 500
    ? "O servidor não conseguiu responder. Tente novamente em instantes."
    : "Não foi possível concluir a ação.";
}

async function chamar<T>(caminho: string, opcoes: RequestInit = {}): Promise<T> {
  const token = sessao.ler();
  let resposta: Response;
  try {
    resposta = await fetch(`${BASE}${caminho}`, {
      ...opcoes,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...opcoes.headers,
      },
    });
  } catch {
    throw new ApiError(0, "Sem conexão com o servidor. Verifique sua internet e tente novamente.");
  }
  const corpo = await resposta.json().catch(() => null);
  if (!resposta.ok) throw new ApiError(resposta.status, mensagemDeErro(corpo, resposta.status));
  return corpo as T;
}

const json = (dados: unknown): RequestInit => ({ body: JSON.stringify(dados) });

export const api = {
  cadastrar: (d: { nome: string; email: string; senha: string; aceite_lgpd: boolean }) =>
    chamar<{ token: string; usuario: Usuario }>("/auth/cadastro", { method: "POST", ...json(d) }),
  entrar: (d: { email: string; senha: string }) =>
    chamar<{ token: string; usuario: Usuario }>("/auth/login", { method: "POST", ...json(d) }),
  eu: () => chamar<Usuario>("/auth/eu"),
  perfil: () => chamar<Perfil>("/perfil"),
  salvarPerfil: (d: Perfil) => chamar<Perfil>("/perfil", { method: "PUT", ...json(d) }),
  criarBusca: (d: NovaBusca) => chamar<Busca>("/buscas", { method: "POST", ...json(d) }),
  consultarBusca: (id: number) => chamar<Busca>(`/buscas/${id}`),
  cancelarBusca: (id: number) => chamar<Busca>(`/buscas/${id}/cancelar`, { method: "POST" }),
  oportunidades: (filtros: { q?: string; status_contato?: string; nivel_certeza?: string }) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([chave, valor]) => valor && params.set(chave, valor));
    const consulta = params.toString();
    return chamar<{ total: number; itens: Oportunidade[] }>(
      `/oportunidades${consulta ? `?${consulta}` : ""}`,
    );
  },
  oportunidade: (id: number) => chamar<OportunidadeDetalhe>(`/oportunidades/${id}`),
};
