import type { ReactNode } from "react";
import { Logo } from "./Icones";
import { SeloCerteza } from "./Selos";

/** Estrutura comum das telas "Entrar" e "Criar conta". */
export function PaginaEntrada({ children }: { children: ReactNode }) {
  return (
    <div className="pagina-entrada">
      <main className="entrada">
        <section>
          <div className="marca">
            <Logo />
            <span>
              <span className="marca-nome">LeadForge</span>
              <br />
              <span className="marca-sub">Copiloto Comercial</span>
            </span>
          </div>
          <h1>Encontre clientes que realmente precisam do seu serviço</h1>
          <p className="lead">
            Copiloto comercial para freelancers de desenvolvimento web. Oportunidades locais com
            evidências reais e o nível de certeza de cada conclusão.
          </p>
          <div className="cartao exemplo" aria-label="Exemplo de evidência">
            <div className="exemplo-topo">
              <span>Exemplo de oportunidade</span>
              <SeloCerteza nivel="sinal_forte" />
            </div>
            <p>
              <strong>Clínica Bela Forma</strong> · Sorocaba, SP
            </p>
            <div className="destaque-evidencia">
              Sem versão para celular (viewport ausente) e sem botão de WhatsApp na página inicial.
            </div>
          </div>
        </section>
        <section>{children}</section>
      </main>
      <footer className="rodape-entrada">
        LeadForge · Projeto de TCC, ADS FATEC Sorocaba · Usamos apenas informações públicas de empresas.
      </footer>
    </div>
  );
}
