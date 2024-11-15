/**
 * @file api.ts
 *
 * This file wraps the API calls to the backend server.
 */

import queryString from "query-string";
import { APIRetrieveResponseType, WrapAPI } from "./types";

/**
 * TODO(!)
 */
export const callRetrieve = async (
  query: string,
  topK: number,
): Promise<WrapAPI<APIRetrieveResponseType>> => {
  const params = queryString.stringify({ query, top_k: topK });
  try {
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/retrieve?${params}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const res = (await response.json()) as APIRetrieveResponseType;
    return { payload: res };
  } catch (e: unknown) {
    if (typeof e === "string") {
      return { error: e };
    } else if (e instanceof Error) {
      return { error: e.message };
    } else {
      return { error: "Unknown error" };
    }
  }
};
