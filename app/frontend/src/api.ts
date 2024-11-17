/**
 * @file api.ts
 *
 * This file wraps the API calls to the backend server.
 */

import queryString from "query-string";
import {
  APIChatResponseType,
  APIRetrieveResponseType,
  ModelType,
  WrapAPI,
} from "./types";

/**
 * Fetch the response from the given URL.
 */
const getResponse = async (url: string) => {
  return await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};

/**
 * Format an unknown error into a string.
 */
const formatError = (error: unknown) => {
  if (typeof error === "string") {
    return error;
  } else if (error instanceof Error) {
    return error.message;
  } else {
    return "Unknown error";
  }
};

/**
 * Format a non-OK response into a string.
 */
const formatNonOkResponse = async (response: Response) => {
  const errorRes = (await response.json()) as { details: string };
  return `Status ${response.status} (${response.statusText}); caused by:\n\n${errorRes.details}`;
};

/**
 * Call the /retrieve backend API.
 */
export const callRetrieve = async (
  query: string,
  topK: number,
): Promise<WrapAPI<APIRetrieveResponseType>> => {
  const params = queryString.stringify({ query, top_k: topK });
  const url = `${import.meta.env.VITE_BACKEND_URL}/retrieve?${params}`;
  try {
    const response = await getResponse(url);
    if (!response.ok) {
      return { error: await formatNonOkResponse(response) };
    }
    const res = (await response.json()) as APIRetrieveResponseType;
    return { payload: res };
  } catch (e: unknown) {
    console.error(e);
    return { error: formatError(e) };
  }
};

/**
 * Call the /chat/{model}/{item_id} backend API.
 */
export const callChat = async (
  query: string,
  model: ModelType,
  id: string,
): Promise<WrapAPI<APIChatResponseType>> => {
  const params = queryString.stringify({ query });
  const url = `${import.meta.env.VITE_BACKEND_URL}/chat/${model}/${id}?${params}`;
  try {
    const response = await getResponse(url);
    if (!response.ok) {
      return { error: await formatNonOkResponse(response) };
    }
    const res = (await response.json()) as APIChatResponseType;
    return { payload: res };
  } catch (e: unknown) {
    console.error(e);
    return { error: formatError(e) };
  }
};
