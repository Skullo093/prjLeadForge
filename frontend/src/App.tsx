import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { RotaProtegida } from "./components/RotaProtegida";
import { CriarConta } from "./pages/CriarConta";
import { Entrar } from "./pages/Entrar";
import { NovaBusca } from "./pages/NovaBusca";
import { Oportunidades } from "./pages/Oportunidades";
import { Perfil } from "./pages/Perfil";

export function App() {
  return (
    <Routes>
      <Route path="/entrar" element={<Entrar />} />
      <Route path="/criar-conta" element={<CriarConta />} />
      <Route element={<RotaProtegida />}>
        <Route element={<Layout />}>
          <Route path="/oportunidades" element={<Oportunidades />} />
          <Route path="/nova-busca" element={<NovaBusca />} />
          <Route path="/perfil" element={<Perfil />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/oportunidades" replace />} />
    </Routes>
  );
}
