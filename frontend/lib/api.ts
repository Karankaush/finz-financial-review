const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function uploadTransactions(
  file: File
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/ingestion/transactions`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to upload transactions"
    );
  }

  return response.json();
}


export async function runClassification() {
  const response = await fetch(
    `${API_BASE_URL}/api/classification/run`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to classify transactions"
    );
  }

  return response.json();
}


export async function getPnL() {
  const response = await fetch(
    `${API_BASE_URL}/api/financial/pnl`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch P&L"
    );
  }

  return response.json();
}


export async function getReviewTransactions() {
  const response = await fetch(
    `${API_BASE_URL}/api/transactions/review`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch review transactions"
    );
  }

  return response.json();
}


export async function correctTransaction(
  id: number,
  category: string,
  accountingTreatment: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/transactions/${id}/classification`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        category,
        accounting_treatment:
          accountingTreatment,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to update transaction"
    );
  }

  return response.json();
}


export async function getVariance(
  previousMonth: string,
  currentMonth: string
) {
  const params = new URLSearchParams({
    previous_month: previousMonth,
    current_month: currentMonth,
  });

  const response = await fetch(
    `${API_BASE_URL}/api/financial/variance?${params}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch variance"
    );
  }

  return response.json();
}


export async function askAnalyst(
  question: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/analyst/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to query AI analyst"
    );
  }

  return response.json();
}