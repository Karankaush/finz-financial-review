"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react";


import {
  uploadTransactions,
  runClassification,
  getPnL,
  askAnalyst,
} from "@/lib/api";


export default function Home() {
  const [file, setFile] =
    useState<File | null>(null);

  const [message, setMessage] =
    useState("");

  const [pnl, setPnl] =
    useState<any[]>([]);

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");


  async function handleUpload() {
    if (!file) return;

    try {
      const result =
        await uploadTransactions(file);

      setMessage(
        `${result.total_transactions} transactions uploaded`
      );
    } catch (error) {
      setMessage(
        "Upload failed"
      );
    }
  }


  async function handleClassification() {
    try {
      const result =
        await runClassification();

      setMessage(
        `${result.classified_transactions} transactions classified. ${result.transactions_needing_review} need review.`
      );
    } catch {
      setMessage(
        "Classification failed"
      );
    }
  }


  async function handlePnL() {
    try {
      const result =
        await getPnL();

      setPnl(result);
    } catch {
      setMessage(
        "Failed to load P&L"
      );
    }
  }


  async function handleAsk() {
    if (!question.trim()) return;

    try {
      const result =
        await askAnalyst(question);

      setAnswer(result.answer);
    } catch {
      setAnswer(
        "Unable to answer question."
      );
    }
  }


  return (
    <main className="min-h-screen bg-slate-950 text-white">

      <div className="mx-auto max-w-6xl px-6 py-10">

        <header className="mb-10">
          <h1 className="text-4xl font-bold">
            Finz Financial Review
          </h1>

          <p className="mt-2 text-slate-400">
            AI-powered financial analysis
            from transaction data
          </p>
        </header>


        {/* Upload */}

        <section className="mb-8 rounded-xl bg-slate-900 p-6">

          <h2 className="mb-4 text-xl font-semibold">
            1. Ingest Transactions
          </h2>

          <input
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={(event) =>
              setFile(
                event.target.files?.[0] || null
              )
            }
            className="mb-4 block"
          />

          <button
            onClick={handleUpload}
            className="rounded-lg bg-blue-600 px-4 py-2 hover:bg-blue-500"
          >
            Upload
          </button>

        </section>


        {/* Classification */}

        <section className="mb-8 rounded-xl bg-slate-900 p-6">

          <h2 className="mb-4 text-xl font-semibold">
            2. Classify Transactions
          </h2>

          <button
            onClick={handleClassification}
            className="rounded-lg bg-purple-600 px-4 py-2 hover:bg-purple-500"
          >
            Run Classification
          </button>

        </section>


        {/* P&L */}

        <section className="mb-8 rounded-xl bg-slate-900 p-6">

          <div className="mb-4 flex items-center justify-between">

            <h2 className="text-xl font-semibold">
              3. Monthly P&L
            </h2>

            <button
              onClick={handlePnL}
              className="rounded-lg bg-emerald-600 px-4 py-2 hover:bg-emerald-500"
            >
              Refresh P&L
            </button>

          </div>


          {pnl.length > 0 && (

            <div className="overflow-x-auto">

              <table className="w-full text-left">

                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="p-3">
                      Month
                    </th>

                    <th className="p-3">
                      Revenue
                    </th>

                    <th className="p-3">
                      COGS
                    </th>

                    <th className="p-3">
                      Gross Profit
                    </th>

                    <th className="p-3">
                      Operating Expenses
                    </th>

                    <th className="p-3">
                      Operating Profit
                    </th>
                  </tr>
                </thead>

                <tbody>

                  {pnl.map((row) => (

                    <tr
                      key={row.month}
                      className="border-b border-slate-800"
                    >

                      <td className="p-3">
                        {row.month}
                      </td>

                      <td className="p-3">
                        ${row.revenue}
                      </td>

                      <td className="p-3">
                        ${row.cogs}
                      </td>

                      <td className="p-3">
                        ${row.gross_profit}
                      </td>

                      <td className="p-3">
                        ${row.operating_expenses}
                      </td>

                      <td className="p-3 font-semibold">
                        ${row.operating_profit}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* AI Analyst */}

        <section className="rounded-xl bg-slate-900 p-6">

          <h2 className="mb-2 text-xl font-semibold">
            AI Financial Analyst
          </h2>

          <p className="mb-5 text-sm text-slate-400">
            Ask questions about revenue,
            profitability, transactions,
            and financial changes.
          </p>


          <div className="flex gap-3">

            <input
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Why did operating profit change?"
              className="flex-1 rounded-lg bg-slate-800 px-4 py-3 outline-none"
            />

            <button
              onClick={handleAsk}
              className="rounded-lg bg-blue-600 px-5 py-3 hover:bg-blue-500"
            >
              Ask
            </button>

          </div>


          {answer && (

            <div className="mt-6 rounded-lg bg-slate-800 p-5">

              <h3 className="mb-2 font-semibold">
                Analysis
              </h3>

              <div className="text-slate-300">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="mb-4 text-2xl font-bold text-white">
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2 className="mb-3 mt-6 text-xl font-semibold text-white">
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3 className="mb-3 mt-5 text-lg font-semibold text-white">
                        {children}
                      </h3>
                    ),

                    p: ({ children }) => (
                      <p className="mb-4 leading-7">
                        {children}
                      </p>
                    ),

                    ul: ({ children }) => (
                      <ul className="mb-4 list-disc space-y-2 pl-6">
                        {children}
                      </ul>
                    ),

                    ol: ({ children }) => (
                      <ol className="mb-4 list-decimal space-y-2 pl-6">
                        {children}
                      </ol>
                    ),

                    li: ({ children }) => (
                      <li className="leading-6">
                        {children}
                      </li>
                    ),

                    strong: ({ children }) => (
                      <strong className="font-semibold text-white">
                        {children}
                      </strong>
                    ),

                    table: ({ children }) => (
                      <div className="my-5 overflow-x-auto rounded-lg border border-slate-700">
                        <table className="w-full min-w-[700px] text-left text-sm">
                          {children}
                        </table>
                      </div>
                    ),

                    thead: ({ children }) => (
                      <thead className="bg-slate-700/70 text-white">
                        {children}
                      </thead>
                    ),

                    tbody: ({ children }) => (
                      <tbody className="divide-y divide-slate-700">
                        {children}
                      </tbody>
                    ),

                    th: ({ children }) => (
                      <th className="px-4 py-3 font-semibold">
                        {children}
                      </th>
                    ),

                    td: ({ children }) => (
                      <td className="px-4 py-3">
                        {children}
                      </td>
                    ),
                  }}
                >
                  {answer}
                </ReactMarkdown>
              </div>

            </div>

          )}

        </section>


        {message && (
          <div className="fixed bottom-6 right-6 rounded-lg bg-slate-800 px-5 py-3 shadow-lg">
            {message}
          </div>
        )}

      </div>

    </main>
  );
}