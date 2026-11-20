import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth";
import {
  IconeAlvo,
  IconeBusca,
  IconePasta,
  IconePessoa,
  IconeRobo,
  IconeSair,
  IconeMais,
  Logo,
} from "./Icones";

const ITENS = [
  { para: "/oportunidades", rotulo: "Oportunidades", Icone: IconeAlvo },
  { para: "/nova-busca", rotulo: "Nova busca", Icone: IconeBusca },
  { para: "/perfil", rotulo: "Perfil", Icone: IconePessoa },
];
const EM_BREVE = [
  { rotulo: "Carteira", Icone: IconePasta },
  { rotulo: "Assistente", Icone: IconeRobo },
];

const MIGALHAS: Record<string, [string, string]> = {
  "/oportunidades": ["Prospecção", "Oportunidades"],
  "/nova-busca": ["Prospecção", "Nova busca"],
  "/perfil": ["Configurações do usuário", "Perfil"],
};

export function Layout() {
  const { usuario, sair } = useAuth();
  const { pathname } = useLocation();
  const [secao, pagina] = MIGALHAS[pathname] ?? ["Prospecção", ""];

  return (
    <div className="app">
      <aside className="lateral">
        <NavLink to="/oportunidades" className="marca" aria-label="LeadForge, ir para oportunidades">
          <Logo />
          <span>
            <span className="marca-nome">LeadForge</span>
            <br />
            <span className="marca-sub">Copiloto Comercial</span>
          </span>
        </NavLink>
        <NavLink to="/nova-busca" className="btn btn-primario btn-largo">
          <IconeMais /> Nova prospecção
        </NavLink>
        <nav className="menu" aria-label="Principal">
          {ITENS.slice(0, 2).map(({ para, rotulo, Icone }) => (
            <NavLink key={para} to={para} className={({ isActive }) => (isActive ? "ativo" : "")}>
              <Icone /> {rotulo}
            </NavLink>
          ))}
          {EM_BREVE.map(({ rotulo, Icone }) => (
            <span key={rotulo} className="item-desativado" aria-disabled="true">
              <Icone /> {rotulo} <span className="em-breve">Em breve</span>
            </span>
          ))}
          <NavLink to="/perfil" className={({ isActive }) => (isActive ? "ativo" : "")}>
            <IconePessoa /> Perfil
          </NavLink>
        </nav>
        <div className="usuario">
          <span className="email">{usuario?.email}</span>
          <button className="btn" onClick={sair}>
            <IconeSair /> Sair
          </button>
        </div>
      </aside>

      <div className="principal">
        <div className="topo" aria-label="Você está em">
          <span>{secao}</span>
          {pagina && (
            <>
              <span aria-hidden="true">›</span>
              <strong>{pagina}</strong>
            </>
          )}
        </div>
        <main className="conteudo">
          <Outlet />
        </main>
      </div>

      <nav className="nav-inferior" aria-label="Principal (celular)">
        {ITENS.map(({ para, rotulo, Icone }) => (
          <NavLink key={para} to={para} className={({ isActive }) => (isActive ? "ativo" : "")}>
            <Icone /> {rotulo}
          </NavLink>
        ))}
        <button
          type="button"
          onClick={sair}
          style={{ flex: 1, background: "none", border: 0, color: "var(--texto-suave)", fontSize: 11 }}
        >
          <IconeSair /> <br />
          Sair
        </button>
      </nav>
    </div>
  );
}
