import type { TtlCacheEntry, UnixMillis, UserId, YouTubeChannelId, YouTubeVideoId } from "./primitives";
import type {
  ChannelMetadata,
  ChannelSource,
  FeedFilter,
  Note,
  SourceId,
  VideoMetadata,
  VideoOpenRecord,
} from "./domain";

/**
 * LocalStorage 계약(contracts, SoT).
 *
 * MVP 퍼시스턴스는 브라우저 LocalStorage만 사용한다(`docs/product/mvp-spec.md`).
 * 키 네이밍은 버전으로 고정하여, 추후 마이그레이션을 가능하게 한다.
 *
 * YouTube 정책 메모: YouTube API Data를 무기한 저장하지 않는다.
 * API에서 온 메타데이터는 TTL 캐시를 기본으로 한다(`docs/product/youtube-api-policy-notes.md` 참고).
 */
export const LOCAL_STORAGE_SCHEMA_VERSION = 1 as const;

/** MVP 앱에서 사용하는 LocalStorage 키(정식). */
export const LS_KEYS = {
  user: "unote:user:v1",
  sources: "unote:sources:v1",
  notes: "unote:notes:v1",
  video_opens: "unote:video_opens:v1",
  ui_state: "unote:ui_state:v1",
  caches: "unote:caches:v1",
} as const;

/** MVP에서 허용하는 LocalStorage 키 유니온. */
export type LocalStorageKey = (typeof LS_KEYS)[keyof typeof LS_KEYS];

/** 저장되는 익명 유저 아이덴티티(MVP: 로그인 없음). */
export interface StoredUser {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  user_id: UserId;
  created_at: UnixMillis;
}

/** 저장되는 유저 등록 Source (MVP: ChannelSource만). */
export interface StoredSources {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  sources: ChannelSource[];
}

/** `video_id`로 키잉된 Note 저장소(MVP: 1 Video : 1 Note). */
export interface StoredNotes {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  notes_by_video_id: Record<YouTubeVideoId, Note>;
}

/** 최근 열어본 영상 목록(선택 UX). */
export interface StoredVideoOpens {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  items: VideoOpenRecord[];
}

/** UI 상태 저장(피드 필터, 마지막으로 열었던 영상 등). */
export interface StoredUiState {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  feed_filter: FeedFilter;
  filter_source_id?: SourceId;
  last_opened_video_id?: YouTubeVideoId;
}

/**
 * API에서 온 메타데이터를 TTL 캐시로 저장하는 영역.
 *
 * 유저 생성 데이터(Notes/Markers)와 분리해서, 캐시 만료/삭제를 쉽게 하기 위한 구조다.
 */
export interface StoredCaches {
  schema_version: typeof LOCAL_STORAGE_SCHEMA_VERSION;
  channels_by_id: Record<YouTubeChannelId, TtlCacheEntry<ChannelMetadata>>;
  videos_by_id: Record<YouTubeVideoId, TtlCacheEntry<VideoMetadata>>;
}

/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredUserV1 = StoredUser;
/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredSourcesV1 = StoredSources;
/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredNotesV1 = StoredNotes;
/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredVideoOpensV1 = StoredVideoOpens;
/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredUiStateV1 = StoredUiState;
/** `LOCAL_STORAGE_SCHEMA_VERSION === 1` 기준 호환 타입 별칭(이전 네이밍). */
export type StoredCachesV1 = StoredCaches;
