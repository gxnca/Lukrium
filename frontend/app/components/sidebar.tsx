"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";
import React from "react";
import {
  BanknotesIcon,
  MagnifyingGlassIcon,
  ChartBarIcon,
  WrenchIcon,
} from "@heroicons/react/24/outline";

const SideBar = () => {
  const pathname = usePathname();

  const options = [
    { name: "Dashboard", icon: WrenchIcon, link: "/" },
    { name: "Revisão", icon: MagnifyingGlassIcon, link: "/review" },
    { name: "Estatistica", icon: ChartBarIcon, link: "/estatistic" },
    { name: "Gera Preço", icon: BanknotesIcon, link: "/priceGenerator" },
  ];

  return (
    <section className="flex flex-col h-screen w-[295px] md:w-[312px] bg-coral pt-10 px-5">
      <Image
        src={"/images/lukrium.png"}
        alt=""
        width={180}
        height={50}
        className="md:w-[230px] ml-3"
      />

      <li className="h-full items-start justify-start mt-16 gap-6 flex flex-col">
        {options.map((option) => (
          <Link
            key={option.name}
            href={option.link}
            className={`p-3 font-tektur rounded-xl w-60 md:w-64 flex items-center justify-start gap-4 text-white font-bold text-2xl duration-200 ease-linear hover:scale-90 hover:opacity-70 ${option.link == pathname ? "bg-[#D9D9D9]/20" : ""}`}
          >
            <option.icon className="hidden md:block h-7 w-7 text-white" />{" "}
            {option.name}
          </Link>
        ))}
      </li>

      <p className="text-white text-center mb-2 opacity-85">
        © 2025 Hackaloiros 4.0
      </p>
    </section>
  );
};

export default SideBar;
