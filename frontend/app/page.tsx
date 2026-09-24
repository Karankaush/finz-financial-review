"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react";


import {
  uploadTransactions,
  runClassification,
  getPnL,
  askAnalyst,
  getReviewTransactions,
  correctTransaction,
} from "@/lib/api";


export default function Home() {
  const [file, setFile] =
    useState<File | null>(null);

  const [dataLoaded, setDataLoaded] = useState(false);

  const [message, setMessage] =
    useState("");

  const [pnl, setPnl] =
    useState<any[]>([]);

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [reviewTransactions, setReviewTransactions] =
    useState<any[]>([]);

  const [reviewLoading, setReviewLoading] =
    useState(false);


  async function handleUpload() {
  if (!file) {
    setMessage("Please select a file first");
    return;
  }

  try {
    const result = await uploadTransactions(file);

    setDataLoaded(true);

    setMessage(
      `${result.total_transactions} transactions uploaded successfully`
    );
  } catch (error) {
    console.error(error);
    setMessage("Upload failed");
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


  async function handleLoadReview() {
  try {
    setReviewLoading(true);

    const result =
      await getReviewTransactions();

    setReviewTransactions(result);
  } catch {
    setMessage(
      "Failed to load review transactions"
    );
  } finally {
    setReviewLoading(false);
  }
  }

  async function handleCorrection(
  id: number,
  category: string,
  accountingTreatment: string
) {
  try {
    await correctTransaction(
      id,
      category,
      accountingTreatment
    );

    setReviewTransactions(
      (current) =>
        current.filter(
          (transaction) =>
            transaction.id !== id
        )
    );

    setMessage(
      "Transaction corrected successfully"
    );
  } catch {
    setMessage(
      "Failed to correct transaction"
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

          <h2 className="mb-2 text-xl font-semibold">
            1. Ingest Transactions
          </h2>

          <p className="mb-5 text-sm text-slate-400">
            Upload your bank transaction file to begin the financial review.
          </p>

          <div className="flex flex-wrap items-center gap-4">

            <label className="cursor-pointer rounded-lg border border-slate-600 bg-slate-800 px-4 py-2 text-sm hover:bg-slate-700">
              Choose File

              <input
                type="file"
                accept=".xlsx,.xls,.csv"
                className="hidden"
                onChange={(event) => {
                  const selectedFile =
                    event.target.files?.[0] ?? null;

                  setFile(selectedFile);
                  setMessage("");
                }}
              />
            </label>

            <button
              type="button"
              onClick={handleUpload}
              disabled={!file}
              className="cursor-pointer rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Upload
            </button>

          </div>

          {file && (
            <div className="mt-4 rounded-lg bg-slate-800 px-4 py-3 text-sm">
              <span className="text-slate-400">
                Selected file:
              </span>{" "}
              <span className="font-medium text-white">
                {file.name}
              </span>
            </div>
          )}

          {dataLoaded && (
            <div className="mt-4 rounded-lg border border-emerald-700 bg-emerald-950/30 px-4 py-3 text-sm text-emerald-300">
              ✓ Dataset loaded successfully
            </div>
          )}

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

        {/* Review Transactions */}

        <section className="mb-8 rounded-xl bg-slate-900 p-6">

          <div className="mb-5 flex items-center justify-between">

            <div>
              <h2 className="text-xl font-semibold">
                3. Transactions Needing Review
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Review and correct uncertain transaction
                classifications.
              </p>
            </div>

            <button
              onClick={handleLoadReview}
              className="rounded-lg bg-amber-600 px-4 py-2 hover:bg-amber-500"
            >
              Load Review Queue
            </button>

          </div>


          {reviewLoading && (
            <p className="text-slate-400">
              Loading review transactions...
            </p>
          )}


          {!reviewLoading &&
            reviewTransactions.length === 0 && (
              <div className="rounded-lg border border-slate-700 p-5 text-center">
                <p className="text-emerald-400">
                  No transactions require review.
                </p>
              </div>
            )}


          {reviewTransactions.length > 0 && (

            <div className="overflow-x-auto">

              <table className="w-full text-left text-sm">

                <thead>
                  <tr className="border-b border-slate-700">

                    <th className="px-3 py-3">
                      Transaction
                    </th>

                    <th className="px-3 py-3">
                      Date
                    </th>

                    <th className="px-3 py-3">
                      Description
                    </th>

                    <th className="px-3 py-3">
                      Amount
                    </th>

                    <th className="px-3 py-3">
                      Confidence
                    </th>

                    <th className="px-3 py-3">
                      Category
                    </th>

                    <th className="px-3 py-3">
                      Accounting
                    </th>

                    <th className="px-3 py-3">
                      Action
                    </th>

                  </tr>
                </thead>


                <tbody className="divide-y divide-slate-800">

                  {reviewTransactions.map(
                    (transaction) => (

                      <ReviewRow
                        key={transaction.id}
                        transaction={transaction}
                        onCorrect={handleCorrection}
                      />

                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

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


function ReviewRow({
  transaction,
  onCorrect,
}: {
  transaction: any;
  onCorrect: (
    id: number,
    category: string,
    accountingTreatment: string
  ) => void;
}) {
  const [category, setCategory] =
    useState("");

  const [accountingTreatment, setAccountingTreatment] =
    useState("P&L");


  return (
    <tr>

      <td className="px-3 py-4 font-medium text-white">
        {transaction.transaction_id}
      </td>


      <td className="px-3 py-4 text-slate-300">
        {transaction.date}
      </td>


      <td className="max-w-xs px-3 py-4 text-slate-300">
        {transaction.description}
      </td>


      <td className="px-3 py-4 whitespace-nowrap">
        ${transaction.amount}
      </td>


      <td className="px-3 py-4">
        <span className="rounded bg-red-900/40 px-2 py-1 text-red-300">
          {Number(
            transaction.confidence
          ).toFixed(2)}
        </span>
      </td>


      <td className="px-3 py-4">

        <select
          value={category}
          onChange={(event) =>
            setCategory(event.target.value)
          }
          className="rounded-lg bg-slate-800 px-3 py-2 text-white outline-none"
        >

          <option value="">
            Select category
          </option>

          <option value="Revenue">
            Revenue
          </option>

          <option value="Food">
            Food
          </option>

          <option value="Beverage">
            Beverage
          </option>

          <option value="Payroll">
            Payroll
          </option>

          <option value="Rent">
            Rent
          </option>

          <option value="Utilities">
            Utilities
          </option>

          <option value="Marketing">
            Marketing
          </option>

          <option value="Insurance">
            Insurance
          </option>

          <option value="Cleaning">
            Cleaning
          </option>

          <option value="Delivery Commission">
            Delivery Commission
          </option>

          <option value="Refunds & Discounts">
            Refunds & Discounts
          </option>

          <option value="Equipment">
            Equipment
          </option>

          <option value="Loan Repayment">
            Loan Repayment
          </option>

          <option value="Owner Distribution">
            Owner Distribution
          </option>

          <option value="Sales Tax">
            Sales Tax
          </option>

        </select>

      </td>


      <td className="px-3 py-4">

        <select
          value={accountingTreatment}
          onChange={(event) =>
            setAccountingTreatment(
              event.target.value
            )
          }
          className="rounded-lg bg-slate-800 px-3 py-2 text-white outline-none"
        >

          <option value="P&L">
            P&L
          </option>

          <option value="Balance Sheet">
            Balance Sheet
          </option>

          <option value="Equity">
            Equity
          </option>

        </select>

      </td>


      <td className="px-3 py-4">

        <button
          disabled={!category}
          onClick={() =>
            onCorrect(
              transaction.id,
              category,
              accountingTreatment
            )
          }
          className="rounded-lg bg-emerald-600 px-3 py-2 text-sm font-medium hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Correct
        </button>

      </td>

    </tr>
  );
}